"""Módulo de Gerenciamento e Persistência de Tarefas do LAY Orchestrator.

Fornece persistência atômica baseada em arquivos (.lay/tasks/), controle de concorrência,
máquina de estados finita e classificação heurística de complexidade.
Opera sem dependência de serviços externos, bancos de dados ou chamadas a modelos.
"""
from __future__ import annotations

import contextlib
import datetime
import json
import os
import re
import sys
import time
import unicodedata
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

TASK_ID_REGEX = re.compile(r"^task-[a-z0-9]{8,16}$")
VALID_COMPLEXITIES = {"low", "medium", "high", "critical"}
VALID_TASK_STATUSES = {"pending", "in_progress", "completed", "failed", "blocked", "escalated"}
VALID_RESULT_STATUSES = {"success", "failure", "needs_clarification", "escalated"}
VALID_EXECUTION_MODES = {"session", "subagent", "arbitrator"}
MAX_PAYLOAD_BYTES = 1024 * 1024  # 1 MB

ROOT_DIR = Path(__file__).resolve().parent.parent

# 11 perfis canônicos de domínio e seus respectivos subagentes
ALL_CANONICAL_DOMAINS = {
    "routing-and-proxy",
    "frontend",
    "engineering",
    "context",
    "devops",
    "qa",
    "security",
    "creative-3d",
    "documentation",
    "design",
    "database",
}

DOMAIN_TO_SPECIALIST = {
    "routing-and-proxy": "lay-omniroute",
    "frontend": "lay-frontend",
    "engineering": "lay-engenharia",
    "context": "lay-contexto",
    "devops": "lay-devops",
    "qa": "lay-qa",
    "security": "lay-seguranca",
    "creative-3d": "lay-3d",
    "documentation": "lay-documentacao",
    "design": "lay-design",
    "database": "lay-banco-de-dados",
}

SPECIALIST_TO_DOMAIN = {v: k for k, v in DOMAIN_TO_SPECIALIST.items()}
SPECIALIST_TO_DOMAIN["lay-arbitro"] = "architecture"
SPECIALIST_TO_DOMAIN["lay-arbitro-opus"] = "architecture"

ALL_CANONICAL_SPECIALISTS = set(SPECIALIST_TO_DOMAIN.keys())

READONLY_SPECIALISTS = {
    "lay-contexto",
    "lay-seguranca",
    "lay-banco-de-dados",
    "lay-arbitro",
    "lay-arbitro-opus",
}

# Suporte de clientes a delegação nativa de subagentes
VALID_CLIENTS = {"claude", "antigravity", "codex", "local"}
CLIENT_DELEGATION_SUPPORT = {
    "claude": True,
    "antigravity": True,
    "codex": False,    # Manter Codex indisponível funcionalmente
    "local": False,    # Ambiente local/CLI sem runtime de subagente
}

DOMAIN_KEYWORDS = {
    "creative-3d": ["3d", "webgl", "blender", "shader", "vanta", "render", "threejs", "three.js", "rigging"],
    "database": ["banco", "database", "sql", "postgres", "mysql", "tabela", "coluna", "migracao", "esquema", "query"],
    "security": ["seguranca", "security", "vulnerab", "cve", "semgrep", "auditoria", "auth", "token", "jwt", "permissao", "api key", "secret"],
    "qa": ["teste", "test", "tdd", "playwright", "devtools", "cobertura", "benchmark", "fixture", "e2e"],
    "devops": ["devops", "ci/cd", "pipeline", "deploy", "vercel", "commit", "branch", "release", "rollout", "git"],
    "frontend": ["frontend", "ui", "ux", "react", "next", "componente", "layout", "css", "tailwind", "animacao", "acessibilidade", "wcag", "html", "card", "padding", "button", "modal", "dialog"],
    "context": ["contexto", "grafo", "ast", "prompt", "rtk", "requisito", "planejamento", "quebra de tarefa"],
    "documentation": ["documentacao", "doc", "adr", "readme", "escrita", "artigo", "polimento", "guia"],
    "routing-and-proxy": ["omniroute", "proxy", "gateway", "roteador", "trafego de rede"],
    "design": ["design", "brandkit", "mockup", "identidade visual", "tipografia", "paleta", "tokens visuais"],
}

DESTRUCTIVE_DEVOPS_KEYWORDS = {"deploy", "push", "release", "reset", "rollback", "force"}
DESTRUCTIVE_DATABASE_KEYWORDS = {"migracao", "drop", "alter", "schema", "esquema", "truncate"}

TERMINAL_EXECUTION_KEYWORDS = {
    "executar", "rodar", "run", "terminal", "bash", "cli", "comando",
    "instalar", "scan cli", "varredura cli", "execucao"
}

ARCHITECTURAL_IMPASSE_KEYWORDS = {
    "impasse", "trade-off", "tradeoff", "dilema", "opcoes conflitantes",
    "conflito de arquitetura", "conflito arquitetural", "decisao entre",
    "escolha entre", "arbitragem", "arbitr"
}

VALID_TRANSITIONS: Dict[str, set[str]] = {
    "pending": {"in_progress"},
    "in_progress": {"completed", "failed", "blocked", "escalated"},
    "blocked": {"in_progress", "failed"},
    "escalated": {"in_progress", "failed"},
    "failed": {"in_progress"},  # Permite tentativa de recuperação / retry
    "completed": set(),         # Estado terminal imutável
}

CRITICAL_KEYWORDS = {
    "arquitetura", "migracao", "migra", "breaking change", "drop table", "esquema banco",
    "perda de dados", "trade-off", "tradeoff", "arbitr", "licenca", "shader complexo", "rig 3d"
}

HIGH_KEYWORDS = {
    "seguranca", "vulnerab", "cve", "semgrep", "auditoria", "performance",
    "concorrencia", "pipeline", "ci/cd", "release gate", "refatora transversal", "transversal"
}

LOW_KEYWORDS = {
    "ajust", "padding", "corrig", "typo", "fix", "pequeno", "cosmetic",
    "docstring", "comentario", "formata", "prop"
}

MEDIUM_KEYWORDS = {
    "componente", "hook", "endpoint", "rota", "api", "tabela", "integracao", "estilo", "teste de integracao"
}


class ConcurrencyError(Exception):
    """Exceção levantada quando uma operação concorrente impede acesso a uma tarefa."""
    pass


class TaskValidationError(ValueError):
    """Exceção levantada para payload ou transição de tarefa inválida."""
    pass


class TaskNotFoundError(FileNotFoundError):
    """Exceção levantada quando uma tarefa solicitada não existe no workspace."""
    pass


def now_iso() -> str:
    """Retorna timestamp UTC atual no formato ISO 8601."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def normalize_text(text: str) -> str:
    """Normaliza texto removendo acentuação e convertendo para minúsculas."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def is_process_alive(pid: int) -> bool:
    """Verifica se um processo com o PID fornecido está ativo no sistema operacional."""
    if pid <= 0:
        return False
    if sys.platform == "win32":
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            SYNCHRONIZE = 0x00100000
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE, False, pid)
            if handle:
                WAIT_TIMEOUT = 0x00000102
                res = ctypes.windll.kernel32.WaitForSingleObject(handle, 0)
                ctypes.windll.kernel32.CloseHandle(handle)
                return res == WAIT_TIMEOUT
            err = ctypes.GetLastError()
            if err == 5:  # ERROR_ACCESS_DENIED: processo existe e está ativo no sistema
                return True
            return False
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


def get_process_start_time(pid: int) -> Optional[float]:
    """Retorna o timestamp UTC de início do processo (Windows) ou None."""
    if pid <= 0:
        return None
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if not handle:
                return None
            creation_time = wintypes.FILETIME()
            exit_time = wintypes.FILETIME()
            kernel_time = wintypes.FILETIME()
            user_time = wintypes.FILETIME()
            ok = ctypes.windll.kernel32.GetProcessTimes(
                handle,
                ctypes.byref(creation_time),
                ctypes.byref(exit_time),
                ctypes.byref(kernel_time),
                ctypes.byref(user_time),
            )
            ctypes.windll.kernel32.CloseHandle(handle)
            if ok:
                ft = (creation_time.dwHighDateTime << 32) + creation_time.dwLowDateTime
                return (ft - 116444736000000000) / 10000000.0
            return None
        except Exception:
            return None
    else:
        try:
            stat_path = Path(f"/proc/{pid}/stat")
            if stat_path.exists():
                return stat_path.stat().st_ctime
        except Exception:
            pass
        return None


def validate_task_id(task_id: str) -> None:
    """Valida formato estrito de ID para prevenir injeção ou path traversal."""
    if not isinstance(task_id, str) or not TASK_ID_REGEX.match(task_id):
        raise TaskValidationError(
            f"ID de tarefa inválido: '{task_id}'. Deve seguir estritamente o formato 'task-[a-z0-9]{{8,16}}'."
        )


def validate_task_path(tasks_dir: Path, file_path: Path) -> None:
    """Valida se o caminho do arquivo reside estritamente dentro do diretório autorizado de tarefas."""
    try:
        file_path.resolve().relative_to(tasks_dir.resolve())
    except ValueError:
        raise TaskValidationError(
            f"Violação de isolamento: caminho '{file_path}' fora do diretório autorizado '{tasks_dir}'."
        )


def get_tasks_dir(workspace: Path) -> Path:
    """Retorna o diretório de tarefas do workspace, criando a pasta se necessário.

    Protege projetos externos de versionamento acidental criando .lay/.gitignore
    sem modificar o .gitignore da raiz do projeto.
    """
    resolved_ws = workspace.resolve()
    lay_dir = (resolved_ws / ".lay").resolve()
    lay_dir.mkdir(parents=True, exist_ok=True)

    lay_gitignore = lay_dir / ".gitignore"
    if not lay_gitignore.exists():
        try:
            lay_gitignore.write_text("# Arquivos locais de tarefas do LAY Orchestrator\n*\n", encoding="utf-8")
        except OSError:
            pass

    tasks_dir = (lay_dir / "tasks").resolve()
    tasks_dir.mkdir(parents=True, exist_ok=True)
    return tasks_dir


@contextlib.contextmanager
def task_lock(workspace: Path, task_id: str, timeout_seconds: float = 3.0):
    """Context manager para controle de concorrência com lock atômico baseado em arquivo.

    Garante que uma operação nunca remova o lock de outro processo através de tokens
    únicos por aquisição e valida vivacidade e reutilização de PID antes de descartar stale locks.
    """
    validate_task_id(task_id)
    tasks_dir = get_tasks_dir(workspace)
    lock_path = tasks_dir / f"{task_id}.lock"
    validate_task_path(tasks_dir, lock_path)
    start_time = time.time()
    my_token = uuid.uuid4().hex
    acquired = False

    while True:
        try:
            # Tenta criar o arquivo de lock de forma atômica e exclusiva
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                payload = {
                    "pid": os.getpid(),
                    "token": my_token,
                    "created_at": now_iso(),
                    "task_id": task_id,
                }
                json.dump(payload, f)
            acquired = True
            break
        except FileExistsError:
            # O lock existe: inspecionar o processo proprietário
            owner_pid = -1
            lock_token = None
            created_at_str = None
            try:
                raw = lock_path.read_text(encoding="utf-8")
                lock_info = json.loads(raw)
                owner_pid = int(lock_info.get("pid", -1))
                lock_token = lock_info.get("token")
                created_at_str = lock_info.get("created_at")
            except (json.JSONDecodeError, UnicodeDecodeError):
                # O arquivo pode estar sendo gravado concorrentemente neste instante
                try:
                    mtime = lock_path.stat().st_mtime
                    if time.time() - mtime < 1.0:
                        # Recém-criado: aguarda escrita do processo concorrente
                        time.sleep(0.05)
                        continue
                except Exception:
                    pass
            except Exception:
                pass

            pid_alive = is_process_alive(owner_pid) if owner_pid > 0 else False
            pid_reused = False

            if pid_alive and created_at_str:
                try:
                    lock_created_ts = datetime.datetime.fromisoformat(created_at_str).timestamp()
                    proc_start = get_process_start_time(owner_pid)
                    if proc_start is not None and proc_start > lock_created_ts + 1.0:
                        # Processo nasceu após a criação do lock -> PID foi reutilizado
                        pid_reused = True
                except Exception:
                    pass

            if pid_alive and not pid_reused:
                # Processo legítimo ainda ativo: aguardar ou falhar se estourar o timeout
                if time.time() - start_time > timeout_seconds:
                    raise ConcurrencyError(
                        f"Tarefa '{task_id}' bloqueada concorrentemente pelo processo ativo PID {owner_pid}."
                    )
                time.sleep(0.05)
            else:
                # Processo morto, inexistente ou PID reutilizado: recuperação segura do lock órfão.
                # Só desvincula se o lock ainda contiver os dados do stale lock identificado
                try:
                    if lock_token:
                        raw_check = lock_path.read_text(encoding="utf-8")
                        check_info = json.loads(raw_check)
                        if check_info.get("token") == lock_token:
                            lock_path.unlink(missing_ok=True)
                    else:
                        lock_path.unlink(missing_ok=True)
                except Exception:
                    pass
                time.sleep(0.02)
        except Exception as e:
            if isinstance(e, ConcurrencyError):
                raise
            raise ConcurrencyError(f"Erro ao obter lock da tarefa '{task_id}': {e}") from e

    try:
        yield
    finally:
        if acquired:
            # Garante que NUNCA remova o lock de outro processo
            try:
                raw = lock_path.read_text(encoding="utf-8")
                info = json.loads(raw)
                if info.get("token") == my_token:
                    lock_path.unlink(missing_ok=True)
            except Exception:
                pass


def atomic_write_task(workspace: Path, task_data: dict) -> None:
    """Grava o payload JSON da tarefa de forma atômica no mesmo volume usando rename."""
    task_id = task_data.get("id", "")
    validate_task_id(task_id)
    tasks_dir = get_tasks_dir(workspace)
    target_path = tasks_dir / f"{task_id}.json"
    validate_task_path(tasks_dir, target_path)

    raw_json = json.dumps(task_data, indent=2, ensure_ascii=False) + "\n"
    encoded = raw_json.encode("utf-8")
    if len(encoded) > MAX_PAYLOAD_BYTES:
        raise TaskValidationError(f"Payload da tarefa excede o limite de {MAX_PAYLOAD_BYTES} bytes.")

    tmp_path = tasks_dir / f"{task_id}.tmp.{uuid.uuid4().hex}"
    validate_task_path(tasks_dir, tmp_path)
    try:
        tmp_path.write_bytes(encoded)
        os.replace(str(tmp_path), str(target_path))
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass


def classify_task(
    title: str,
    description: str = "",
    files: Optional[List[str]] = None,
    explicit_complexity: Optional[str] = None
) -> Dict[str, Any]:
    """Classifica a complexidade e modo de execução heurísticamente sem chamadas a modelos."""
    if explicit_complexity is not None:
        c = explicit_complexity.lower().strip()
        if c not in VALID_COMPLEXITIES:
            raise TaskValidationError(f"Complexidade explícita inválida: '{explicit_complexity}'. Opções: {sorted(VALID_COMPLEXITIES)}")
        complexity = c
        if complexity == "critical":
            recommended_mode = "arbitrator"
            rationale = "Classificação crítica definida manualmente pelo usuário."
        elif complexity == "high":
            recommended_mode = "session"
            rationale = "Classificação alta definida manualmente; recomenda-se resolução na sessão com decomposição em etapas."
        else:
            recommended_mode = "session"
            rationale = f"Classificação {complexity} definida manualmente; resolução recomendada na sessão atual."
        return {
            "complexity": complexity,
            "recommended_mode": recommended_mode,
            "rationale": rationale,
            "suggests_persistence": True,
        }

    # Análise heurística textual normalizada
    norm = normalize_text(f"{title} {description}")

    if any(k in norm for k in CRITICAL_KEYWORDS):
        complexity = "critical"
        recommended_mode = "arbitrator"
        rationale = "Decisão arquitetural, trade-off de alto impacto ou risco estrutural detectado."
        suggests_persistence = True
    elif any(k in norm for k in HIGH_KEYWORDS):
        complexity = "high"
        recommended_mode = "session"
        rationale = "Demanda com complexidade técnica elevada; recomendada decomposição em etapas na sessão."
        suggests_persistence = True
    elif any(k in norm for k in LOW_KEYWORDS):
        complexity = "low"
        recommended_mode = "session"
        rationale = "Demanda pontual com resolução recomendada na sessão atual sem subagentes."
        suggests_persistence = False
    elif any(k in norm for k in MEDIUM_KEYWORDS):
        complexity = "medium"
        recommended_mode = "session"
        rationale = "Escopo moderado; resolução padrão na sessão atual ativando a skill de domínio pertinente."
        suggests_persistence = True
    else:
        complexity = "low"
        recommended_mode = "session"
        rationale = "Demanda pontual com resolução recomendada na sessão atual sem subagentes."
        suggests_persistence = False

    return {
        "complexity": complexity,
        "recommended_mode": recommended_mode,
        "rationale": rationale,
        "suggests_persistence": suggests_persistence,
    }


def validate_task_schema(data: dict) -> None:
    """Valida estaticamente se os campos e tipos da tarefa estão em conformidade com o schema."""
    if not isinstance(data, dict):
        raise TaskValidationError("Dados da tarefa devem ser um objeto JSON.")

    required_fields = ["schema_version", "id", "title", "complexity", "status", "routing", "handoff", "timestamps"]
    for field in required_fields:
        if field not in data:
            raise TaskValidationError(f"Campo obrigatório ausente na tarefa: '{field}'")

    validate_task_id(data["id"])

    if data["complexity"] not in VALID_COMPLEXITIES:
        raise TaskValidationError(f"Complexidade inválida: '{data['complexity']}'")

    if data["status"] not in VALID_TASK_STATUSES:
        raise TaskValidationError(f"Status inválido: '{data['status']}'")

    routing = data.get("routing", {})
    if not isinstance(routing, dict) or "execution_mode" not in routing or "client" not in routing:
        raise TaskValidationError("Objeto 'routing' inválido ou incompleto.")
    if routing["execution_mode"] not in VALID_EXECUTION_MODES:
        raise TaskValidationError(f"Modo de execução inválido: '{routing['execution_mode']}'")

    handoff = data.get("handoff", {})
    if not isinstance(handoff, dict):
        raise TaskValidationError("Objeto 'handoff' deve ser um dicionário.")
    for hf in ["task", "domain", "context", "constraints", "acceptance_criteria"]:
        if hf not in handoff:
            raise TaskValidationError(f"Campo obrigatório ausente em handoff: '{hf}'")

    result = data.get("result")
    if result is not None:
        if not isinstance(result, dict):
            raise TaskValidationError("Objeto 'result' deve ser um dicionário ou null.")
        if "status" not in result or result["status"] not in VALID_RESULT_STATUSES:
            raise TaskValidationError(f"Status do resultado inválido: '{result.get('status')}'")
        if not result.get("summary") or not isinstance(result["summary"], str):
            raise TaskValidationError("Campo 'summary' em 'result' deve ser uma string não vazia.")


def infer_domain(text: str) -> str:
    """Infere deterministicamente o domínio canônico a partir do texto normalizado."""
    norm = normalize_text(text)

    # Avalia domínios especializados por ordem de prioridade
    priority_order = [
        "creative-3d",
        "database",
        "security",
        "qa",
        "devops",
        "routing-and-proxy",
        "context",
        "documentation",
        "design",
        "frontend",
    ]
    for dom in priority_order:
        keywords = DOMAIN_KEYWORDS.get(dom, [])
        if any(k in norm for k in keywords):
            return dom

    return "engineering"


def get_relevant_skills(
    domain: str,
    text: str = "",
    root: Optional[Path] = None,
    limit: int = 4
) -> List[str]:
    """Descobre e pontua skills públicas do repositório para a finalidade concreta da tarefa.

    Retorna lista vazia se nenhuma skill atingir relevância concreta suficiente,
    evitando sugestões artificiais ou descontextualizadas.
    """
    target_root = root or ROOT_DIR
    domain_dir = target_root / "refactored_skills" / domain
    if not domain_dir.exists() or not domain_dir.is_dir():
        return []

    available = []
    for p in sorted(domain_dir.iterdir()):
        if p.is_dir() and (p / "SKILL.md").exists():
            available.append(p.name)

    if not available or not text.strip():
        return []

    norm = normalize_text(text)
    stop_parts = {
        "and", "the", "with", "for", "of", "in", "to", "a", "an",
        "de", "do", "da", "em", "para", "com", "um", "uma", "os", "as"
    }
    scored = []
    for s in available:
        parts = [p for p in s.split("-") if len(p) > 2 and p not in stop_parts]
        score = sum(2 if p in norm else (1 if len(p) >= 5 and p[:4] in norm else 0) for p in parts)
        if score >= 2:
            scored.append((score, s))

    if not scored:
        return []

    scored.sort(key=lambda x: (-x[0], x[1]))
    return [s[1] for s in scored[:limit]]


def recommend_task_routing(
    title: str,
    description: str = "",
    domain: Optional[str] = None,
    client: str = "local",
    context_files: Optional[List[str]] = None,
    explicit_complexity: Optional[str] = None,
    explicit_specialist: Optional[str] = None,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    """Produz uma recomendação verificável de roteamento, domínio, skills e modo de execução."""
    if not title or not title.strip():
        raise TaskValidationError("O título da tarefa não pode ser vazio.")

    # 1. Validação do cliente
    client_norm = (client or "local").lower().strip()
    if client_norm not in VALID_CLIENTS:
        raise TaskValidationError(
            f"Cliente inválido: '{client}'. Clientes suportados: {sorted(VALID_CLIENTS)}"
        )
    delegation_allowed = CLIENT_DELEGATION_SUPPORT.get(client_norm, False)

    # 2. Validação ou inferência de domínio
    combined_text = f"{title} {description}"
    if domain:
        d = domain.lower().strip()
        if d not in ALL_CANONICAL_DOMAINS:
            raise TaskValidationError(
                f"Domínio inválido: '{domain}'. Domínios canônicos permitidos: {sorted(ALL_CANONICAL_DOMAINS)}"
            )
        target_domain = d
    else:
        target_domain = infer_domain(combined_text)

    # 3. Classificação de complexidade
    clf = classify_task(title=title, description=description, explicit_complexity=explicit_complexity)
    complexity = clf["complexity"]

    # 4. Resolução e validação de especialista
    if explicit_specialist:
        s = explicit_specialist.strip()
        if s not in ALL_CANONICAL_SPECIALISTS:
            raise TaskValidationError(
                f"Especialista inválido: '{explicit_specialist}'. Especialistas canônicos permitidos: {sorted(ALL_CANONICAL_SPECIALISTS)}"
            )
        target_specialist = s
    else:
        target_specialist = DOMAIN_TO_SPECIALIST.get(target_domain, "lay-engenharia")

    # 5. Política de execução e delegação mínima
    norm_text = normalize_text(combined_text)
    requires_authorization = False

    requires_terminal = any(k in norm_text for k in TERMINAL_EXECUTION_KEYWORDS)
    has_impasse = any(k in norm_text for k in ARCHITECTURAL_IMPASSE_KEYWORDS)

    is_security_reading = (
        target_domain == "security"
        and any(k in norm_text for k in ["auditoria", "vulnerab", "cve", "semgrep", "revisao", "inspecao"])
        and not requires_terminal
    )
    is_database_reading = (
        target_domain == "database"
        and any(k in norm_text for k in ["integridade", "esquema", "analise", "consistencia"])
        and not requires_terminal
    )
    is_3d_specialized = target_domain == "creative-3d" and any(k in norm_text for k in ["blender", "shader", "webgl"])

    if complexity == "critical":
        # Tarefa crítica: exige autorização explícita
        requires_authorization = True
        if has_impasse:
            # Impasse arquitetural real: arbitragem indicada como possibilidade justificada
            if delegation_allowed:
                recommended_mode = "arbitrator"
                target_specialist = "lay-arbitro" if client_norm == "antigravity" else "lay-arbitro-opus"
                rationale = (
                    "Impasse arquitetural / trade-off estrutural detectado. "
                    "Arbitragem indicada como possibilidade justificada para parecer técnico, "
                    "sujeita a autorização humana explícita antes da convocação."
                )
            else:
                recommended_mode = "session"
                rationale = (
                    f"Impasse crítico identificado, porém o cliente '{client_norm}' não suporta arbitragem/subagentes; "
                    "resolução deve ser conduzida na sessão sob supervisão humana."
                )
        else:
            # Tarefa crítica sem impasse: EXECUÇÃO PADRÃO MANTIDA NA SESSÃO
            recommended_mode = "session"
            target_specialist = DOMAIN_TO_SPECIALIST.get(target_domain, "lay-engenharia")
            rationale = (
                f"Demanda crítica de alto impacto no domínio '{target_domain}'. "
                "Execução padrão mantida na sessão atual sob supervisão humana direta. "
                "Se houver impasse entre alternativas concorrentes, a arbitragem pode ser convocada sob autorização."
            )
    elif not delegation_allowed:
        recommended_mode = "session"
        if client_norm == "codex":
            rationale = (
                "Cliente 'codex' indisponível funcionalmente para delegação nesta versão; "
                f"resolução restrita à sessão atual para o domínio '{target_domain}'."
            )
        else:
            rationale = (
                f"Ambiente '{client_norm}' sem suporte nativo a delegação de subagentes; "
                f"resolução recomendada na sessão atual para o domínio '{target_domain}'."
            )
    elif target_domain == "security" and requires_terminal:
        # lay-seguranca é estritamente somente-leitura e não possui Bash
        recommended_mode = "session"
        rationale = (
            "A tarefa requer execução de ferramentas externas via terminal (ex: Semgrep). "
            "Como 'lay-seguranca' possui exclusivamente ferramentas de leitura (Read, Grep, Glob) "
            "sem acesso a terminal (Bash), a execução da ferramenta deve ocorrer na sessão atual "
            "(ou relatórios previamente gerados devem ser submetidos para revisão estática)."
        )
    elif target_domain == "database" and requires_terminal:
        # lay-banco-de-dados é estritamente somente-leitura e não possui Bash
        recommended_mode = "session"
        requires_authorization = True
        rationale = (
            "A tarefa requer execução de scripts/comandos de banco via terminal. "
            "Como 'lay-banco-de-dados' opera estritamente como somente-leitura (Read, Grep, Glob), "
            "a execução deve ocorrer na sessão atual com supervisão humana direta."
        )
    elif is_security_reading:
        recommended_mode = "subagent"
        rationale = (
            "Demanda de análise estática e auditoria de código por leitura beneficia-se de "
            f"isolamento operacional estrito (sandbox somente-leitura sem escrita) via '{target_specialist}'."
        )
    elif is_database_reading:
        recommended_mode = "subagent"
        rationale = (
            "Demanda de análise estática de esquema de banco de dados beneficia-se de "
            f"isolamento operacional estrito via '{target_specialist}'."
        )
    elif is_3d_specialized:
        recommended_mode = "subagent"
        rationale = (
            f"Demanda gráfica/3D requer ambiente especializado de renderização via '{target_specialist}'."
        )
    elif complexity == "high":
        # Complexidade alta NÃO implica delegação obrigatória
        recommended_mode = "session"
        rationale = (
            f"Demanda de complexidade alta. Recomenda-se resolução estruturada na sessão atual "
            f"com decomposição em etapas, ativando as skills do domínio '{target_domain}'."
        )
    elif complexity == "low":
        recommended_mode = "session"
        rationale = "Demanda pontual com resolução recomendada na sessão atual sem subagentes."
    else:
        recommended_mode = "session"
        rationale = f"Política padrão: resolução na sessão atual utilizando as skills pertinentes de '{target_domain}'."

    # 6. Checagem de necessidade de autorização (operações de risco)
    if target_domain == "devops" and any(k in norm_text for k in DESTRUCTIVE_DEVOPS_KEYWORDS):
        requires_authorization = True
    elif target_domain == "database" and any(k in norm_text for k in DESTRUCTIVE_DATABASE_KEYWORDS):
        requires_authorization = True

    # 7. Descoberta de skills relevantes
    skills = get_relevant_skills(target_domain, text=combined_text, root=root)

    return {
        "complexity": complexity,
        "recommended_domain": target_domain,
        "relevant_skills": skills,
        "current_client": client_norm,
        "recommended_mode": recommended_mode,
        "recommended_specialist": target_specialist,
        "rationale": rationale,
        "requires_authorization": requires_authorization,
        "delegation_allowed": delegation_allowed,
    }


def create_task(
    workspace: Path,
    title: str,
    domain: Optional[str] = None,
    complexity: Optional[str] = None,
    context: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    acceptance_criteria: Optional[List[str]] = None,
    client: str = "local"
) -> Dict[str, Any]:
    """Cria e persiste uma nova tarefa de forma atômica."""
    if not title or not title.strip():
        raise TaskValidationError("O título da tarefa não pode ser vazio.")

    rec = recommend_task_routing(
        title=title,
        domain=domain,
        client=client,
        explicit_complexity=complexity
    )
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    created_time = now_iso()

    task_data = {
        "schema_version": 1,
        "id": task_id,
        "title": title.strip(),
        "complexity": rec["complexity"],
        "status": "pending",
        "routing": {
            "client": rec["current_client"],
            "target_specialist": None,
            "execution_mode": rec["recommended_mode"],
            "delegation_reason": None,
        },
        "handoff": {
            "task": title.strip(),
            "domain": rec["recommended_domain"],
            "context": [str(c) for c in (context or [])],
            "constraints": [str(c) for c in (constraints or [])],
            "acceptance_criteria": [str(c) for c in (acceptance_criteria or [])],
        },
        "result": None,
        "timestamps": {
            "created_at": created_time,
            "updated_at": created_time,
            "completed_at": None,
        },
    }

    validate_task_schema(task_data)
    with task_lock(workspace, task_id):
        atomic_write_task(workspace, task_data)

    return task_data


def get_task(workspace: Path, task_id: str) -> Dict[str, Any]:
    """Recupera e valida os dados de uma tarefa existente."""
    validate_task_id(task_id)
    tasks_dir = get_tasks_dir(workspace)
    task_path = tasks_dir / f"{task_id}.json"
    validate_task_path(tasks_dir, task_path)
    if not task_path.exists():
        raise TaskNotFoundError(f"Tarefa não encontrada: '{task_id}' em {workspace}")

    try:
        raw = task_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise TaskValidationError(f"Arquivo da tarefa corrompido ou JSON inválido: {e}") from e

    validate_task_schema(data)
    return data


def list_tasks(workspace: Path, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lista tarefas persistidas no workspace com filtro opcional por status."""
    tasks_dir = get_tasks_dir(workspace)
    task_files = sorted(tasks_dir.glob("task-*.json"))
    tasks = []

    for f in task_files:
        try:
            raw = f.read_text(encoding="utf-8")
            data = json.loads(raw)
            validate_task_schema(data)
            if status_filter and data.get("status") != status_filter:
                continue
            tasks.append(data)
        except Exception:
            # Arquivos corrompidos ou não-tarefas são ignorados na listagem
            continue

    # Ordena decrescente por data de criação
    tasks.sort(key=lambda t: t.get("timestamps", {}).get("created_at", ""), reverse=True)
    return tasks


def assign_task(
    workspace: Path,
    task_id: str,
    specialist: str,
    mode: str = "session",
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Atribui responsável e modalidade de execução à tarefa com controle de concorrência."""
    validate_task_id(task_id)
    if specialist not in ALL_CANONICAL_SPECIALISTS:
        raise TaskValidationError(
            f"Especialista inválido: '{specialist}'. Especialistas canônicos permitidos: {sorted(ALL_CANONICAL_SPECIALISTS)}"
        )

    if mode not in VALID_EXECUTION_MODES:
        raise TaskValidationError(f"Modo de execução inválido: '{mode}'. Opções: {sorted(VALID_EXECUTION_MODES)}")

    if mode in ("subagent", "arbitrator") and (not reason or not reason.strip()):
        raise TaskValidationError(
            f"Atribuição para modalidade '{mode}' exige justificativa objetiva (--reason) conforme política de delegação mínima."
        )

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)

        client = task.get("routing", {}).get("client", "local").lower()
        if mode in ("subagent", "arbitrator"):
            if client == "codex":
                raise TaskValidationError(
                    "Delegação de subagentes indisponível para o cliente 'codex' nesta versão. Use modo 'session'."
                )
            if client == "local":
                raise TaskValidationError(
                    "Delegação de subagentes indisponível para o cliente 'local'. O modo deve ser 'session'."
                )

        current_status = task["status"]
        if current_status == "completed":
            raise TaskValidationError(f"Não é permitido reatribuir a tarefa concluída '{task_id}'.")

        # Atualiza roteamento
        task["routing"]["target_specialist"] = specialist
        task["routing"]["execution_mode"] = mode
        task["routing"]["delegation_reason"] = reason.strip() if reason else None

        # Se estava pendente, transita para em progresso
        if current_status == "pending":
            task["status"] = "in_progress"

        task["timestamps"]["updated_at"] = now_iso()
        validate_task_schema(task)
        atomic_write_task(workspace, task)

    return task


def update_task_status(workspace: Path, task_id: str, new_status: str) -> Dict[str, Any]:
    """Atualiza o status de uma tarefa respeitando a máquina de estados finita."""
    validate_task_id(task_id)
    if new_status not in VALID_TASK_STATUSES:
        raise TaskValidationError(f"Status inválido: '{new_status}'. Opções: {sorted(VALID_TASK_STATUSES)}")

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)
        current_status = task["status"]

        if new_status == current_status:
            return task

        allowed = VALID_TRANSITIONS.get(current_status, set())
        if new_status not in allowed:
            raise TaskValidationError(
                f"Transição de estado inválida: de '{current_status}' para '{new_status}'. "
                f"Transições permitidas a partir de '{current_status}': {sorted(allowed) if allowed else 'nenhuma (estado terminal)'}."
            )

        task["status"] = new_status
        task["timestamps"]["updated_at"] = now_iso()
        validate_task_schema(task)
        atomic_write_task(workspace, task)

    return task


def complete_task(
    workspace: Path,
    task_id: str,
    summary: str,
    result_status: str = "success",
    artifacts: Optional[List[str]] = None,
    open_items: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Conclui a tarefa gravando o contrato RESULT e atualizando timestamps."""
    validate_task_id(task_id)
    if not summary or not summary.strip():
        raise TaskValidationError("A conclusão de uma tarefa exige um resumo conclusivo não vazio (--summary).")

    if result_status not in VALID_RESULT_STATUSES:
        raise TaskValidationError(f"Status do resultado inválido: '{result_status}'. Opções: {sorted(VALID_RESULT_STATUSES)}")

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)
        current_status = task["status"]

        if current_status == "completed":
            raise TaskValidationError(f"A tarefa '{task_id}' já está concluída.")

        # Transição permitida: de in_progress, blocked ou escalated para completed
        allowed_completion = {"in_progress", "blocked", "escalated"}
        if current_status not in allowed_completion:
            raise TaskValidationError(
                f"Não é permitido concluir tarefa no estado '{current_status}'. A tarefa deve estar em progresso."
            )

        task["status"] = "completed"
        task["result"] = {
            "status": result_status,
            "summary": summary.strip(),
            "artifacts": [str(a) for a in (artifacts or [])],
            "open_items": [str(item) for item in (open_items or [])],
        }
        completion_time = now_iso()
        task["timestamps"]["updated_at"] = completion_time
        task["timestamps"]["completed_at"] = completion_time

        validate_task_schema(task)
        atomic_write_task(workspace, task)

    return task

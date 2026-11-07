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
VALID_EXECUTION_MODES = {"session", "subagent", "cross_client", "arbitrator"}
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

CLIENT_COMPATIBLE_SPECIALISTS = {
    "claude": {
        "lay-omniroute", "lay-frontend", "lay-engenharia", "lay-contexto",
        "lay-devops", "lay-qa", "lay-seguranca", "lay-3d",
        "lay-documentacao", "lay-design", "lay-banco-de-dados",
        "lay-arbitro-opus"
    },
    "antigravity": {
        "lay-omniroute", "lay-frontend", "lay-engenharia", "lay-contexto",
        "lay-devops", "lay-qa", "lay-seguranca", "lay-3d",
        "lay-documentacao", "lay-design", "lay-banco-de-dados",
        "lay-arbitro"
    },
    "codex": set(),
    "local": set(),
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
    "blocked": {"in_progress", "failed", "escalated"},
    "escalated": {"in_progress", "failed"},
    "failed": {"in_progress"},  # Permite tentativa de recuperação / retry
    "completed": set(),         # Estado terminal imutável
}

RESULT_STATUS_TO_TASK_STATUS: Dict[str, str] = {
    "success": "completed",
    "failure": "failed",
    "needs_clarification": "blocked",
    "escalated": "escalated",
}

MAX_ARBITRATION_TOKENS: int = 15000

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
    if routing.get("source_client") is not None and routing["source_client"] not in VALID_CLIENTS:
        raise TaskValidationError(f"Cliente de origem inválido: '{routing['source_client']}'")

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
        if not result.get("summary") or not isinstance(result["summary"], str) or len(result["summary"].strip()) < 3:
            raise TaskValidationError("Campo 'summary' em 'result' deve ser uma string substantiva (mínimo 3 caracteres).")

    history = data.get("history")
    if history is not None:
        if not isinstance(history, list):
            raise TaskValidationError("Campo 'history' deve ser uma lista ou null.")
        for idx, entry in enumerate(history):
            if not isinstance(entry, dict):
                raise TaskValidationError(f"Entrada de histórico #{idx} deve ser um objeto.")
            for req in ["timestamp", "previous_status", "action"]:
                if req not in entry:
                    raise TaskValidationError(f"Campo obrigatório '{req}' ausente na entrada de histórico #{idx}.")

    arbitration = data.get("arbitration")
    if arbitration is not None:
        if not isinstance(arbitration, dict):
            raise TaskValidationError("Campo 'arbitration' deve ser um objeto ou null.")
        if "rounds_count" in arbitration and not isinstance(arbitration["rounds_count"], int):
            raise TaskValidationError("Campo 'rounds_count' em 'arbitration' deve ser um inteiro.")
        if "packages" in arbitration:
            if not isinstance(arbitration["packages"], list):
                raise TaskValidationError("Campo 'packages' em 'arbitration' deve ser uma lista.")
            for p_idx, pkg in enumerate(arbitration["packages"]):
                if not isinstance(pkg, dict):
                    raise TaskValidationError(f"Pacote de arbitragem #{p_idx} deve ser um objeto.")
                for req in ["round", "problem", "alternatives", "requires_authorization", "created_at"]:
                    if req not in pkg:
                        raise TaskValidationError(f"Campo obrigatório '{req}' ausente no pacote de arbitragem #{p_idx}.")
                if len(pkg.get("alternatives", [])) < 2:
                    raise TaskValidationError(f"Pacote #{p_idx} deve conter ao menos 2 alternativas concorrentes.")


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
    target_client: Optional[str] = None,
    complexity: Optional[str] = None,
    root: Optional[Path] = None,
) -> Dict[str, Any]:
    """Produz uma recomendação verificável de roteamento seguindo a hierarquia de decisão:
    1. Sessão atual com skills relevantes (padrão).
    2. Subagente nativo, somente quando justificado (isolamento estrito read-only ou 3D).
    3. Outro cliente (cross-client handoff), quando necessário e autorizado.
    4. Árbitro, exclusivamente diante de impasse real e autorização explícita.
    """
    if not title or not title.strip():
        raise TaskValidationError("O título da tarefa não pode ser vazio.")

    # 1. Validação dos clientes
    client_norm = (client or "local").lower().strip()
    if client_norm not in VALID_CLIENTS:
        raise TaskValidationError(
            f"Cliente inválido: '{client}'. Clientes suportados: {sorted(VALID_CLIENTS)}"
        )
    delegation_allowed = CLIENT_DELEGATION_SUPPORT.get(client_norm, False)

    target_client_norm = (target_client or "").lower().strip() if target_client else None
    if target_client_norm and target_client_norm not in VALID_CLIENTS:
        raise TaskValidationError(
            f"Cliente alvo inválido: '{target_client}'. Clientes suportados: {sorted(VALID_CLIENTS)}"
        )

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
    clf = classify_task(title=title, description=description, explicit_complexity=explicit_complexity or complexity)
    complexity = clf["complexity"]

    # 4. Resolução e validação de especialista
    if explicit_specialist:
        s = explicit_specialist.strip()
        if s not in ALL_CANONICAL_SPECIALISTS:
            raise TaskValidationError(
                f"Especialista inválido: '{explicit_specialist}'. Especialistas canônicos permitidos: {sorted(ALL_CANONICAL_SPECIALISTS)}"
            )
        if client_norm in CLIENT_COMPATIBLE_SPECIALISTS and s not in CLIENT_COMPATIBLE_SPECIALISTS[client_norm]:
            if client_norm == "antigravity" and s == "lay-arbitro-opus":
                raise TaskValidationError("Especialista 'lay-arbitro-opus' é específico do Claude Code. No Google Antigravity, utilize 'lay-arbitro'.")
            if client_norm == "claude" and s == "lay-arbitro":
                raise TaskValidationError("Especialista 'lay-arbitro' é específico do Antigravity. No Claude Code, utilize 'lay-arbitro-opus'.")
            if client_norm in ("codex", "local"):
                raise TaskValidationError(f"Delegação de especialista indisponível para o cliente '{client_norm}'.")
            raise TaskValidationError(f"Especialista '{s}' incompatível com o cliente '{client_norm}'.")
        target_specialist = s
    else:
        target_specialist = DOMAIN_TO_SPECIALIST.get(target_domain, "lay-engenharia")

    # 5. Política de execução seguindo a ordem de precedência estrita
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
        # 4. Árbitro / Tarefa Crítica
        requires_authorization = True
        if has_impasse:
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
            recommended_mode = "session"
            target_specialist = DOMAIN_TO_SPECIALIST.get(target_domain, "lay-engenharia")
            rationale = (
                f"Demanda crítica de alto impacto no domínio '{target_domain}'. "
                "Execução padrão mantida na sessão atual sob supervisão humana direta. "
                "Se houver impasse entre alternativas concorrentes, a arbitragem pode ser convocada sob autorização."
            )
    elif target_client_norm and target_client_norm != client_norm:
        # 3. Outro cliente (Cross-Client Handoff), quando necessário e autorizado
        if target_client_norm == "codex":
            recommended_mode = "session"
            rationale = (
                "Cliente 'codex' indisponível funcionalmente para delegação/handoff nesta versão; "
                f"resolução mantida na sessão atual para o domínio '{target_domain}'."
            )
        else:
            recommended_mode = "cross_client"
            requires_authorization = True
            if target_specialist in ("lay-arbitro", "lay-arbitro-opus"):
                target_specialist = "lay-arbitro" if target_client_norm == "antigravity" else "lay-arbitro-opus"
            rationale = (
                f"Handoff entre clientes recomendado ('{client_norm}' -> '{target_client_norm}'). "
                "Operação requer autorização humana explícita antes do despacho."
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
        recommended_mode = "session"
        rationale = (
            "A tarefa requer execução de ferramentas externas via terminal (ex: Semgrep). "
            "Como 'lay-seguranca' possui exclusivamente ferramentas de leitura (Read, Grep, Glob) "
            "sem acesso a terminal (Bash), a execução da ferramenta deve ocorrer na sessão atual "
            "(ou relatórios previamente gerados devem ser submetidos para revisão estática)."
        )
    elif target_domain == "database" and requires_terminal:
        recommended_mode = "session"
        requires_authorization = True
        rationale = (
            "A tarefa requer execução de scripts/comandos de banco via terminal. "
            "Como 'lay-banco-de-dados' opera estritamente como somente-leitura (Read, Grep, Glob), "
            "a execução deve ocorrer na sessão atual com supervisão humana direta."
        )
    elif is_security_reading:
        # 2. Subagente nativo, somente quando justificado (isolamento estrito read-only)
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
        # 1. Sessão atual com skills relevantes (padrão)
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
        "target_client": target_client_norm or client_norm,
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
            "source_client": None,
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
    """Atribui responsável e modalidade de execução à tarefa com controle de concorrência e compatibilidade estrita."""
    validate_task_id(task_id)
    if specialist not in ALL_CANONICAL_SPECIALISTS:
        raise TaskValidationError(
            f"Especialista inválido: '{specialist}'. Especialistas canônicos permitidos: {sorted(ALL_CANONICAL_SPECIALISTS)}"
        )

    if mode not in VALID_EXECUTION_MODES:
        raise TaskValidationError(f"Modo de execução inválido: '{mode}'. Opções: {sorted(VALID_EXECUTION_MODES)}")

    if mode in ("subagent", "arbitrator", "cross_client") and (not reason or not reason.strip()):
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

            compat = CLIENT_COMPATIBLE_SPECIALISTS.get(client, set())
            if specialist not in compat:
                if client == "antigravity" and specialist == "lay-arbitro-opus":
                    raise TaskValidationError("Especialista 'lay-arbitro-opus' é específico do Claude Code. No Google Antigravity, utilize 'lay-arbitro'.")
                if client == "claude" and specialist == "lay-arbitro":
                    raise TaskValidationError("Especialista 'lay-arbitro' é específico do Antigravity. No Claude Code, utilize 'lay-arbitro-opus'.")
                raise TaskValidationError(f"Especialista '{specialist}' incompatível com o cliente '{client}'.")

        # Validação de coerência do modo árbitro
        if mode == "arbitrator" and specialist not in ("lay-arbitro", "lay-arbitro-opus"):
            raise TaskValidationError(
                f"Modo 'arbitrator' requer especialista árbitro ('lay-arbitro' ou 'lay-arbitro-opus'), recebido '{specialist}'."
            )
        if specialist in ("lay-arbitro", "lay-arbitro-opus") and mode != "arbitrator":
            raise TaskValidationError(
                f"Especialista árbitro '{specialist}' só pode ser atribuído na modalidade 'arbitrator'."
            )

        # Validação de incompatibilidade operacional com ferramentas (somente em subagent)
        if mode in ("subagent", "cross_client"):
            task_text = f"{task['title']} {' '.join(task.get('handoff', {}).get('constraints', []))}"
            norm_title = normalize_text(task_text)
            if specialist == "lay-banco-de-dados" and any(k in norm_title for k in DESTRUCTIVE_DATABASE_KEYWORDS):
                raise TaskValidationError(
                    "Incompatibilidade operacional: especialista 'lay-banco-de-dados' opera estritamente como somente-leitura "
                    "e não executa migrações destrutivas. Conduza na sessão sob supervisão humana."
                )
            if specialist in READONLY_SPECIALISTS and any(k in norm_title for k in TERMINAL_EXECUTION_KEYWORDS):
                raise TaskValidationError(
                    f"Incompatibilidade de ferramentas: especialista '{specialist}' possui perfil estritamente somente-leitura "
                    "e não tem acesso a ferramentas de terminal (Bash/CLI). A execução deve ocorrer na sessão atual."
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



def validate_artifact_paths(
    workspace: Path,
    artifacts: List[str],
    check_existence: bool = False
) -> None:
    """Valida integridade estrutural, limites do workspace e existência física de artefatos.

    - Rejeita strings vazias ou nulas.
    - Impede path traversal e escapes do workspace via '..' ou symlinks/junctions.
    - Se check_existence=True: verifica se o artefato realmente existe e é um arquivo físico regular.
    - Não executa nem interpreta nenhum arquivo como código ou comando.
    """
    if not artifacts:
        return

    ws_resolved = workspace.resolve()

    for art in artifacts:
        if not art or not isinstance(art, str) or not art.strip():
            raise TaskValidationError("Caminho de artefato inválido: não pode ser vazio ou conter apenas espaços.")

        art_clean = art.strip()
        p_raw = Path(art_clean)

        if p_raw.is_absolute():
            p_target = p_raw.resolve()
        else:
            p_target = (ws_resolved / p_raw).resolve()

        # Verifica se o caminho escapa do workspace
        try:
            p_target.relative_to(ws_resolved)
        except ValueError:
            raise TaskValidationError(
                f"Violação de isolamento de workspace: artefato '{art_clean}' escapa do diretório autorizado do projeto."
            )

        if p_target == ws_resolved:
            raise TaskValidationError(
                f"Artefato inválido: o caminho aponta para a raiz do workspace: '{art_clean}'"
            )

        if check_existence:
            if not p_target.exists():
                raise TaskValidationError(
                    f"Artefato declarado não existe no disco: '{art_clean}'"
                )
            if not p_target.is_file():
                raise TaskValidationError(
                    f"Artefato declarado deve ser um arquivo regular: '{art_clean}'"
                )

def complete_task(
    workspace: Path,
    task_id: str,
    summary: str,
    result_status: str = "success",
    artifacts: Optional[List[str]] = None,
    open_items: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Registra o contrato RESULT e atualiza o ciclo de vida da tarefa.

    Mapeamento consistente de status:
    - success -> completed (terminal e imutável)
    - failure -> failed (permite recuperação controlada)
    - needs_clarification -> blocked (permite retomada após esclarecimento)
    - escalated -> escalated (permite preparação de arbitragem ou retomada)
    """
    validate_task_id(task_id)
    if not summary or not isinstance(summary, str) or len(summary.strip()) < 3:
        raise TaskValidationError("A entrega de resultado exige um resumo substantivo (--summary) com pelo menos 3 caracteres.")

    if result_status not in VALID_RESULT_STATUSES:
        raise TaskValidationError(
            f"Status do resultado inválido: '{result_status}'. Opções permitidas: {sorted(VALID_RESULT_STATUSES)}"
        )

    raw_artifacts = list(artifacts or [])
    clean_open_items = [str(item).strip() for item in (open_items or []) if str(item).strip()]

    # Validação estrutural e de isolamento de todos os artefatos declarados
    # Se o status for success e houver artefatos declarados, verifica obrigatoriamente a existência física
    check_exist = (result_status == "success" and len(raw_artifacts) > 0)
    validate_artifact_paths(workspace, raw_artifacts, check_existence=check_exist)
    clean_artifacts = [str(a).strip() for a in raw_artifacts]

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)
        current_status = task["status"]

        if current_status == "completed":
            raise TaskValidationError(f"A tarefa '{task_id}' já está em estado terminal 'completed' e não pode ser alterada.")

        allowed_origins = {"in_progress", "blocked", "escalated"}
        if current_status not in allowed_origins:
            raise TaskValidationError(
                f"Não é permitido registrar resultado para tarefa no estado '{current_status}'. "
                f"A tarefa deve estar em 'in_progress', 'blocked' ou 'escalated'."
            )

        new_status = RESULT_STATUS_TO_TASK_STATUS[result_status]
        now_ts = now_iso()

        task["status"] = new_status
        task["result"] = {
            "status": result_status,
            "summary": summary.strip(),
            "artifacts": clean_artifacts,
            "open_items": clean_open_items,
        }
        task["timestamps"]["updated_at"] = now_ts
        if new_status == "completed":
            task["timestamps"]["completed_at"] = now_ts

        validate_task_schema(task)
        atomic_write_task(workspace, task)

    return task


def resume_task(
    workspace: Path,
    task_id: str,
    clarification: Optional[str] = None,
    reason: Optional[str] = None
) -> Dict[str, Any]:
    """Retoma controladamente uma tarefa em estado 'blocked', 'failed' ou 'escalated' para 'in_progress'.

    Preserva histórico completo das execuções e resultados anteriores.
    Não executa retentativas automáticas.
    """
    validate_task_id(task_id)

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)
        current_status = task["status"]

        if current_status == "completed":
            raise TaskValidationError(
                f"Não é permitido retomar a tarefa '{task_id}': estado 'completed' é terminal e imutável."
            )

        resumable_statuses = {"blocked", "failed", "escalated"}
        if current_status not in resumable_statuses:
            raise TaskValidationError(
                f"Tarefa '{task_id}' no estado '{current_status}' não pode ser retomada. "
                f"Recuperação permitida exclusivamente a partir de: {sorted(resumable_statuses)}."
            )

        now_ts = now_iso()
        resume_reason = (reason or "").strip()
        clarif_text = (clarification or "").strip()
        history_reason = resume_reason or clarif_text or "Retomada controlada de execução"

        history_entry = {
            "timestamp": now_ts,
            "previous_status": current_status,
            "action": "resume",
            "reason": history_reason,
            "previous_result": task.get("result"),
        }

        history = list(task.get("history") or [])
        history.append(history_entry)
        task["history"] = history

        # Se houver esclarecimento fornecido, anexa ao contexto do handoff
        if clarif_text:
            task["handoff"]["context"].append(f"[Esclarecimento]: {clarif_text}")

        # Limpa o resultado anterior da tarefa para a nova execução
        task["result"] = None
        task["status"] = "in_progress"
        task["timestamps"]["updated_at"] = now_ts

        validate_task_schema(task)
        atomic_write_task(workspace, task)

    return task


def prepare_arbitration_package(
    workspace: Path,
    task_id: str,
    problem: str,
    alternatives: List[str],
    evidences: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    criteria: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Prepara pacote estruturado para arbitragem controlada quando a tarefa for escalada.

    - Requer formulação clara do problema e ao menos 2 alternativas concorrentes viáveis.
    - Limite de até 3 rodadas de arbitragem por tarefa (anti-loop).
    - Respeita o teto heurístico estimado de 15.000 tokens (~60.000 caracteres).
    - Marca explicitamente 'requires_authorization = True'.
    - Não invoca subagentes, árbitros ou modelos externos nesta etapa.
    """
    validate_task_id(task_id)

    if not problem or not isinstance(problem, str) or len(problem.strip()) < 3:
        raise TaskValidationError("Arbitragem exige descrição clara do problema (--problem) com ao menos 3 caracteres.")

    clean_alts = [str(a).strip() for a in (alternatives or []) if str(a).strip()]
    if len(clean_alts) < 2:
        raise TaskValidationError(
            f"Arbitragem exige ao menos 2 alternativas concorrentes viáveis. Fornecidas: {len(clean_alts)}."
        )

    clean_evidences = [str(e).strip() for e in (evidences or []) if str(e).strip()]
    clean_constraints = [str(c).strip() for c in (constraints or []) if str(c).strip()]
    clean_criteria = [str(cr).strip() for cr in (criteria or []) if str(cr).strip()]

    # Estimativa heurística de tokens (~4 caracteres por token)
    all_texts = [problem] + clean_alts + clean_evidences + clean_constraints + clean_criteria
    total_chars = sum(len(t) for t in all_texts)
    estimated_tokens = total_chars // 4

    if estimated_tokens > MAX_ARBITRATION_TOKENS:
        raise TaskValidationError(
            f"Pacote de arbitragem excede o teto heurístico estimado de {MAX_ARBITRATION_TOKENS} tokens "
            f"(estimado: ~{estimated_tokens} tokens / {total_chars} caracteres). "
            "Sintetize as evidências e o problema antes de submeter ao árbitro."
        )

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)
        current_status = task["status"]

        if current_status == "completed":
            raise TaskValidationError(
                f"Não é permitido arbitrar a tarefa '{task_id}': estado 'completed' é terminal e imutável."
            )

        allowed_origins = {"in_progress", "blocked", "escalated"}
        if current_status not in allowed_origins:
            raise TaskValidationError(
                f"Não é permitido preparar arbitragem para tarefa no estado '{current_status}'. "
                f"A tarefa deve estar em: {sorted(allowed_origins)}."
            )

        arbitration_data = task.get("arbitration") or {"rounds_count": 0, "packages": []}
        rounds_count = arbitration_data.get("rounds_count", 0)

        if rounds_count >= 3:
            raise TaskValidationError(
                f"Limite máximo de 3 rodadas de arbitragem atingido para a tarefa '{task_id}'. "
                "Nova arbitragem bloqueada para evitar loops infinitos."
            )

        target_round = rounds_count + 1
        now_ts = now_iso()

        package = {
            "round": target_round,
            "problem": problem.strip(),
            "alternatives": clean_alts,
            "evidences": clean_evidences,
            "constraints": clean_constraints,
            "criteria": clean_criteria,
            "estimated_tokens": estimated_tokens,
            "requires_authorization": True,
            "created_at": now_ts,
        }

        packages = list(arbitration_data.get("packages") or [])
        packages.append(package)

        # Preparação de pacote não consome rodada real (modelos não foram convocados)
        task["arbitration"] = {
            "rounds_count": rounds_count,
            "packages": packages,
        }

        history = list(task.get("history") or [])
        history.append({
            "timestamp": now_ts,
            "previous_status": current_status,
            "action": "arbitrate",
            "reason": f"Pacote de arbitragem preparado (alvo: rodada {target_round}): {problem.strip()}",
            "previous_result": task.get("result"),
        })
        task["history"] = history

        task["status"] = "escalated"
        task["timestamps"]["updated_at"] = now_ts

        validate_task_schema(task)
        atomic_write_task(workspace, task)

    return task


def handoff_task(
    workspace: Path,
    task_id: str,
    target_client: str,
    reason: str,
    authorized: bool = False,
    context: Optional[List[str]] = None,
    execution_mode: Optional[str] = None,
    specialist: Optional[str] = None,
) -> Dict[str, Any]:
    """Transfere uma tarefa entre clientes (Cross-Client Handoff) com rastreabilidade e validação de autorização.

    - Exige autorização explícita (--authorized) para cruzar fronteiras de cliente.
    - Rejeita cliente 'codex' como destino funcional nesta versão.
    - Transfere estritamente o contexto necessário (sem vazamento de memória ou sessão de outro cliente).
    - Preserva task_id, status e histórico completo.
    - Não executa comandos nem invoca modelos nesta etapa.
    """
    validate_task_id(task_id)

    target_norm = (target_client or "").lower().strip()
    if target_norm not in VALID_CLIENTS:
        raise TaskValidationError(
            f"Cliente de destino inválido: '{target_client}'. Clientes suportados: {sorted(VALID_CLIENTS)}"
        )

    if target_norm == "codex":
        raise TaskValidationError(
            "Handoff para o cliente 'codex' indisponível funcionalmente nesta versão."
        )

    if not reason or not isinstance(reason, str) or len(reason.strip()) < 5:
        raise TaskValidationError(
            "Handoff entre clientes exige justificativa técnica objetiva (--reason) com pelo menos 5 caracteres."
        )

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)
        current_status = task["status"]

        if current_status == "completed":
            raise TaskValidationError(
                f"Não é permitido realizar handoff da tarefa concluída '{task_id}': estado terminal e imutável."
            )

        source_client = task.get("routing", {}).get("client", "local").lower()
        if target_norm == source_client:
            raise TaskValidationError(
                f"Handoff redundante: a tarefa já está alocada para o cliente '{target_norm}'."
            )

        # Regra de autorização explícita para cruzar fronteiras de cliente
        if not authorized:
            raise TaskValidationError(
                f"Handoff entre clientes ('{source_client}' -> '{target_norm}') requer autorização explícita (--authorized)."
            )

        now_ts = now_iso()

        # Contexto mínimo transferido (somente o necessário, sem dumping de sessão de outro cliente)
        if context is not None:
            clean_context = [str(c).strip() for c in context if str(c).strip()]
        else:
            clean_context = list(task.get("handoff", {}).get("context", []))

        # Ajuste de especialista caso o especialista anterior seja incompatível com o novo cliente
        current_specialist = specialist or task.get("routing", {}).get("target_specialist")
        if current_specialist:
            if target_norm == "antigravity" and current_specialist == "lay-arbitro-opus":
                current_specialist = "lay-arbitro"
            elif target_norm == "claude" and current_specialist == "lay-arbitro":
                current_specialist = "lay-arbitro-opus"
            elif current_specialist not in CLIENT_COMPATIBLE_SPECIALISTS.get(target_norm, set()):
                current_specialist = None

        new_mode = execution_mode or task.get("routing", {}).get("execution_mode", "session")
        if new_mode not in VALID_EXECUTION_MODES:
            new_mode = "session"

        # Rastreabilidade completa da origem e do destino
        task["routing"]["source_client"] = source_client
        task["routing"]["client"] = target_norm
        task["routing"]["target_specialist"] = current_specialist
        task["routing"]["execution_mode"] = new_mode
        task["routing"]["delegation_reason"] = reason.strip()

        task["handoff"]["context"] = clean_context

        # Histórico de rastreabilidade
        history = list(task.get("history") or [])
        history.append({
            "timestamp": now_ts,
            "previous_status": current_status,
            "action": "cross_client_handoff",
            "reason": reason.strip(),
            "source_client": source_client,
            "target_client": target_norm,
            "previous_result": task.get("result"),
        })
        task["history"] = history

        # Atualiza timestamp
        task["timestamps"]["updated_at"] = now_ts

        # Se estava pending, transita para in_progress
        if current_status == "pending":
            task["status"] = "in_progress"

        validate_task_schema(task)
        atomic_write_task(workspace, task)

    return task

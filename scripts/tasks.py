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
                    elif time.time() - lock_created_ts > 60.0:
                        # Operação atômica em disco retida há mais de 60s -> stale
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


def create_task(
    workspace: Path,
    title: str,
    domain: str = "engineering",
    complexity: Optional[str] = None,
    context: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    acceptance_criteria: Optional[List[str]] = None,
    client: str = "local"
) -> Dict[str, Any]:
    """Cria e persiste uma nova tarefa de forma atômica."""
    if not title or not title.strip():
        raise TaskValidationError("O título da tarefa não pode ser vazio.")

    classification = classify_task(title=title, explicit_complexity=complexity)
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    created_time = now_iso()

    task_data = {
        "schema_version": 1,
        "id": task_id,
        "title": title.strip(),
        "complexity": classification["complexity"],
        "status": "pending",
        "routing": {
            "client": client,
            "target_specialist": None,
            "execution_mode": classification["recommended_mode"],
            "delegation_reason": None,
        },
        "handoff": {
            "task": title.strip(),
            "domain": domain.strip(),
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
    if mode not in VALID_EXECUTION_MODES:
        raise TaskValidationError(f"Modo de execução inválido: '{mode}'. Opções: {sorted(VALID_EXECUTION_MODES)}")

    if mode in ("subagent", "arbitrator") and (not reason or not reason.strip()):
        raise TaskValidationError(
            f"Atribuição para modalidade '{mode}' exige justificativa objetiva (--reason) conforme política de delegação mínima."
        )

    with task_lock(workspace, task_id):
        task = get_task(workspace, task_id)

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

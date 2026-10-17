#!/usr/bin/env bash
# agy-runner.sh — wrapper único para o Google Antigravity CLI (agy), somente OAuth (Google AI Pro).
# Uso:
#   agy-runner.sh check
#   agy-runner.sh media  --prompt-file F --out CAMINHO.(png|webp|jpg) [--transparent] [--model M]
#   agy-runner.sh review --prompt-file F --task ID [--model M] [--effort E] [--out RELATORIO.md]
# Códigos de saída: 0 ok | 2 uso | 10 agy ausente/não autenticado | 11 modelo proibido
#                   12 circuit breaker | 13 mídia não encontrada | 14 alpha falhou | 15 falha do agy
set -uo pipefail

BRAIN_DIR="${AGY_BRAIN_DIR:-$HOME/.gemini/antigravity-cli/brain}"
CONFIG=".claude/antigravity.json"
TIMEOUT_S="${AGY_TIMEOUT_S:-600}"

die() { local code="$1"; shift; echo "agy-runner: $*" >&2; exit "$code"; }
log() { echo "agy-runner: $*" >&2; }

# Regra financeira: nunca usar chaves pagas. Remove-as do ambiente de TODA chamada ao agy.
agy_oauth() {
  env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u GOOGLE_GENAI_USE_VERTEXAI \
      -u GOOGLE_CLOUD_PROJECT -u GOOGLE_APPLICATION_CREDENTIALS agy "$@"
}

native_path() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s' "$1"; fi; }

PY=""
for c in python3 python; do command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys' >/dev/null 2>&1 && { PY="$c"; break; }; done

abs_path() {  # caminho absoluto sem exigir que o arquivo exista
  local p="$1" d b
  d="$(dirname -- "$p")"; b="$(basename -- "$p")"
  mkdir -p -- "$d" || return 1
  printf '%s/%s' "$(cd -- "$d" && pwd)" "$b"
}

json_get() {  # json_get chave.aninhada padrão
  [ -n "$PY" ] && [ -f "$CONFIG" ] || { printf '%s' "$2"; return; }
  "$PY" - "$CONFIG" "$1" "$2" <<'PYEOF'
import json, sys
try:
    v = json.load(open(sys.argv[1], encoding="utf-8"))
    for k in sys.argv[2].split("."):
        v = v[k]
    print(v, end="")
except Exception:
    print(sys.argv[3], end="")
PYEOF
}

check_agy() {
  command -v agy >/dev/null 2>&1 || die 10 "binário 'agy' não encontrado no PATH. Instale o Google Antigravity CLI e faça login com a conta Google AI Pro (OAuth)."
  # 'agy models' consulta a conta; falhar aqui indica sessão OAuth ausente ou expirada.
  agy_oauth models >/dev/null 2>&1 || die 10 "agy não respondeu a 'agy models'. Autentique via OAuth (conta Google AI Pro) e tente de novo. Não use chaves de API."
}

forbid_claude_model() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    *claude*|*sonnet*|*opus*|*haiku*) die 11 "modelo '$1' proibido: o autor do código já é o Claude (diversidade cognitiva). Use gemini-* ou gpt-oss-*." ;;
  esac
}

resolve_model_args() {  # imprime argumentos --model/--effort; usa "<modelo>-<esforço>" quando o agy o lista
  local model="$1" effort="$2" listed
  MODEL_ARGS=()
  [ -z "$model" ] && return 0
  listed="$(agy_oauth models 2>/dev/null | awk '{print $1}')"
  if [ -n "$effort" ] && printf '%s\n' "$listed" | grep -qx -- "$model-$effort"; then
    MODEL_ARGS=(--model "$model-$effort")
  else
    MODEL_ARGS=(--model "$model"); [ -n "$effort" ] && MODEL_ARGS+=(--effort "$effort")
  fi
}

run_agy() {  # run_agy <saída|-> args...  (single-shot, sem retry)
  local out="$1"; shift
  local tcmd=()
  command -v timeout >/dev/null 2>&1 && tcmd=(timeout "$TIMEOUT_S")
  if [ "$out" = "-" ]; then
    "${tcmd[@]}" env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u GOOGLE_GENAI_USE_VERTEXAI -u GOOGLE_CLOUD_PROJECT -u GOOGLE_APPLICATION_CREDENTIALS agy "$@"
  else
    "${tcmd[@]}" env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u GOOGLE_GENAI_USE_VERTEXAI -u GOOGLE_CLOUD_PROJECT -u GOOGLE_APPLICATION_CREDENTIALS agy "$@" >"$out"
  fi
}

# ---------- alpha real ----------
make_transparent() {  # make_transparent <arquivo> : remove fundo sólido liso, salva com alpha real
  local f="$1"
  if command -v rembg >/dev/null 2>&1 && [ "${AGY_ALPHA_ENGINE:-auto}" != "pil" ]; then
    log "alpha: rembg"; rembg i "$f" "$f.alpha.png" 2>/dev/null && { finalize_alpha "$f" "$f.alpha.png"; return $?; }
  fi
  [ -n "$PY" ] || die 14 "sem Python para o pós-processamento alpha (instale python3 + pillow + numpy, ou rembg)."
  log "alpha: PIL/numpy (cor de fundo amostrada nas bordas)"
  "$PY" - "$f" <<'PYEOF' || die 14 "falha no alpha via PIL/numpy (pip install pillow numpy)."
import sys, numpy as np
from PIL import Image
src = sys.argv[1]
im = Image.open(src).convert("RGBA")
a = np.asarray(im).astype(np.float32)
rgb = a[..., :3]
edge = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
bg = np.median(edge, axis=0)
dist = np.sqrt(((rgb - bg) ** 2).sum(axis=2))
lo, hi = 18.0, 60.0                      # tolerância: transparente abaixo de lo, opaco acima de hi
alpha = np.clip((dist - lo) / (hi - lo), 0, 1)
try:                                     # só remove fundo conectado às bordas (preserva miolo parecido com o fundo)
    from scipy import ndimage
    cand = dist < hi
    lab, _ = ndimage.label(cand)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    keep_bg = np.isin(lab, list(border))
    alpha = np.where(keep_bg, alpha, 1.0)
except Exception:
    pass
# remove halo: puxa a cor das bordas semitransparentes para longe da cor de fundo
safe = np.maximum(alpha, 1e-3)[..., None]
rgb2 = np.clip((rgb - bg * (1 - safe)) / safe, 0, 255)
out = np.dstack([np.where(alpha[..., None] > 0, rgb2, rgb), alpha * 255]).astype(np.uint8)
Image.fromarray(out, "RGBA").save(src + ".alpha.png")
PYEOF
  finalize_alpha "$f" "$f.alpha.png"
}

finalize_alpha() {  # converte para o formato do destino (png/webp) e valida que o canal alpha é real
  local dest="$1" tmp="$2" ext
  ext="$(printf '%s' "${dest##*.}" | tr '[:upper:]' '[:lower:]')"
  case "$ext" in png|webp) ;; *) ext="png"; dest="${dest%.*}.png"; log "alpha exige png/webp; destino ajustado para $dest" ;; esac
  [ -n "$PY" ] || { mv -f "$tmp" "$dest"; return 0; }
  "$PY" - "$tmp" "$dest" <<'PYEOF' || die 14 "arquivo final sem alpha real (nenhum pixel transparente)."
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGBA")
lo, hi = im.getchannel("A").getextrema()
if lo >= 250:
    sys.exit(1)
im.save(sys.argv[2], lossless=True) if sys.argv[2].lower().endswith(".webp") else im.save(sys.argv[2])
print(f"alpha ok: min={lo} max={hi}", file=sys.stderr)
PYEOF
  rm -f "$tmp"
  echo "$dest"
}

# ---------- subcomandos ----------
cmd_media() {
  local pf="" out="" transparent=0 model=""
  while [ $# -gt 0 ]; do case "$1" in
    --prompt-file) pf="$2"; shift 2;; --out) out="$2"; shift 2;;
    --transparent) transparent=1; shift;; --model) model="$2"; shift 2;;
    *) die 2 "argumento desconhecido: $1";; esac; done
  [ -f "$pf" ] && [ -n "$out" ] || die 2 "media exige --prompt-file existente e --out"
  [ -n "$model" ] && forbid_claude_model "$model"
  check_agy
  local abs; abs="$(abs_path "$out")" || die 2 "não foi possível criar a pasta de saída"
  local outdir; outdir="$(dirname -- "$abs")"
  resolve_model_args "$model" ""
  local marker; marker="$(mktemp)"
  local prev=""
  if [ -s "$abs" ]; then prev="$abs.prev"; mv -f -- "$abs" "$prev"; fi  # evita tratar saida velha como nova; restaurado se falhar
  local full; full="$(cat "$pf")

OUTPUT REQUIREMENT: generate exactly ONE image and save it to this exact absolute path: $(native_path "$abs")
Do not modify any source code or project file. Do not generate additional variants."
  log "chamando agy (single-shot) → $abs"
  run_agy "$marker.log" -p "$full" --mode accept-edits --add-dir "$(native_path "$outdir")" "${MODEL_ARGS[@]}" \
    || log "agy terminou com código != 0 (veja $marker.log); tentando recuperar mídia do brain"
  if [ ! -s "$abs" ]; then
    log "arquivo ausente no destino; buscando mídia dos últimos 2 min em $BRAIN_DIR"
    local found
    found="$(find "$BRAIN_DIR" -type f \( -iname '*.png' -o -iname '*.webp' -o -iname '*.jpg' -o -iname '*.jpeg' \) -mmin -2 -newer "$marker" -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)"
    [ -n "$found" ] || { tail -n 20 "$marker.log" >&2; rm -f "$marker"; [ -n "$prev" ] && mv -f -- "$prev" "$abs"; die 13 "nenhuma mídia gerada nos últimos 2 min. Não repita em loop: revise o prompt/cota."; }
    local sext dext; sext="$(printf '%s' "${found##*.}" | tr '[:upper:]' '[:lower:]')"; dext="$(printf '%s' "${abs##*.}" | tr '[:upper:]' '[:lower:]')"
    if [ "$sext" != "$dext" ] && [ -n "$PY" ] && "$PY" -c 'import PIL' 2>/dev/null; then
      "$PY" -c 'import sys;from PIL import Image;Image.open(sys.argv[1]).save(sys.argv[2])' "$found" "$abs"
    else
      [ "$sext" != "$dext" ] && { abs="${abs%.*}.$sext"; log "sem PIL para converter; destino ajustado para $abs"; }
      cp -f -- "$found" "$abs"
    fi
    log "recuperado de $found"
  fi
  rm -f "$marker" "$marker.log"
  [ -n "$prev" ] && rm -f -- "$prev"
  local final="$abs"
  if [ "$transparent" -eq 1 ]; then final="$(make_transparent "$abs")" || exit $?; [ "$final" != "$abs" ] && [ -n "$final" ] && [ "${final%.*}" = "${abs%.*}" ] && [ "$final" != "$abs" ] && rm -f "$abs"; fi
  echo "OUTPUT=$final"
  echo "PRÓXIMO PASSO OBRIGATÓRIO: o Claude deve abrir o arquivo com a ferramenta Read e validar contra o contexto da UI." >&2
}

cmd_review() {
  local pf="" task="default" model="" effort="" out=""
  while [ $# -gt 0 ]; do case "$1" in
    --prompt-file) pf="$2"; shift 2;; --task) task="$2"; shift 2;;
    --model) model="$2"; shift 2;; --effort) effort="$2"; shift 2;; --out) out="$2"; shift 2;;
    *) die 2 "argumento desconhecido: $1";; esac; done
  [ -f "$pf" ] || die 2 "review exige --prompt-file existente"
  [ -z "$model" ] && model="$(json_get review_config.model gemini-3.8-flash)"
  [ -z "$effort" ] && effort="$(json_get review_config.effort medium)"
  forbid_claude_model "$model"
  check_agy
  local max; max="$(json_get review_config.max_adversarial_rounds 2)"
  local state=".claude/.agy-rounds"; mkdir -p .claude
  local used; used="$(grep -c "^$task\$" "$state" 2>/dev/null || true)"; used="${used:-0}"
  [ "$used" -lt "$max" ] || die 12 "circuit breaker: $used/$max rodadas já usadas para a tarefa '$task'. Peça decisão humana."
  echo "$task" >> "$state"
  resolve_model_args "$model" "$effort"
  log "rodada $((used+1))/$max, modelo=$model esforço=$effort, mode=plan (somente leitura)"
  local prompt; prompt="$(cat "$pf")"
  if [ -n "$out" ]; then
    run_agy "$out" -p "$prompt" --mode plan "${MODEL_ARGS[@]}" || die 15 "agy falhou na revisão"
    echo "OUTPUT=$out"
  else
    run_agy - -p "$prompt" --mode plan "${MODEL_ARGS[@]}" || die 15 "agy falhou na revisão"
  fi
}

case "${1:-}" in
  check)  check_agy; echo "agy ok (OAuth)";;
  media)  shift; cmd_media "$@";;
  review) shift; cmd_review "$@";;
  *) die 2 "uso: agy-runner.sh {check|media|review} ...";;
esac

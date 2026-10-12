#!/usr/bin/env sh
set -eu
repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$repo_root/scripts/skill_hub.py" install --agents "${1:-all}"
python3 "$repo_root/scripts/skill_hub.py" doctor

#!/usr/bin/env bash
set -euo pipefail
python -m pip install -U pip
pip install -e .
python -m playwright install --with-deps chromium firefox webkit
pytest -n auto --browsers=$(python - <<'PY'
from tests.utils.config import load_settings; print(','.join(load_settings().browsers))
PY
)

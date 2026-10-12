#!/usr/bin/env bash
set -euo pipefail
export PYTHONHASHSEED=0

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUT_DIR="$ROOT_DIR/generated/include/mavlink/v2.0"
DEF_FILE="$ROOT_DIR/message_definitions/v1.0/openhd.xml"

PYTHON_BIN=${PYTHON:-python3}
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN=python
fi

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
"$PYTHON_BIN" "$ROOT_DIR/pymavlink/tools/mavgen.py" \
  --lang C \
  --wire-protocol 2.0 \
  --strict-units \
  --output "$OUT_DIR" \
  "$DEF_FILE"

"$PYTHON_BIN" "$ROOT_DIR/scripts/openhd_wire.py" --output "$ROOT_DIR/generated/wire"
"$PYTHON_BIN" - "$OUT_DIR" <<'PY'
import pathlib, re, sys
for path in pathlib.Path(sys.argv[1]).glob('*/version.h'):
    text = path.read_text()
    text = re.sub(r'#define MAVLINK_BUILD_DATE ".*"', '#define MAVLINK_BUILD_DATE "reproducible"', text)
    path.write_text(text)
PY

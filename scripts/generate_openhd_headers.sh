#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUT_DIR="$ROOT_DIR/generated/include/mavlink/v2.0/openhd"
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

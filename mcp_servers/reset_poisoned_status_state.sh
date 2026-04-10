#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="$ROOT_DIR/state/poisoned_status_state.json"

rm -f "$STATE_FILE"
echo "Removed $STATE_FILE"

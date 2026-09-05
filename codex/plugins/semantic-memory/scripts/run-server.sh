#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export SM_KIT_DEFAULT_DIR="$HOME/.local/share/semantic-memory"
export SM_KIT_DEFAULT_PROFILE="agent"
exec "$SCRIPT_DIR/semantic-memory-launch.sh" "$@"

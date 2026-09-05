#!/usr/bin/env bash
# Host entrypoint only; shared launcher owns all native configuration.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -n "${SEMANTIC_MEMORY_HTTP_TOKEN:-}" ] || [ -n "${SEMANTIC_MEMORY_HTTP_TOKEN_FILE:-}" ]; then
  echo "Use SEMANTIC_MEMORY_HTTP_AUTH_TOKEN_FILE with a private file; legacy Hermes token settings are unsupported" >&2
  exit 64
fi
for arg in "$@"; do
  case "$arg" in --http-auth-token|--http-auth-token=*)
    echo "Direct --http-auth-token is forbidden; use SEMANTIC_MEMORY_HTTP_AUTH_TOKEN_FILE" >&2
    exit 64
  ;; esac
done
exec "$SCRIPT_DIR/../../shared/scripts/run-server.sh" "$@"

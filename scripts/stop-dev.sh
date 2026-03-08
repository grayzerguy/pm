#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for f in .pm_backend.pid .pm_frontend.pid; do
  if [ -f "$ROOT/$f" ]; then
    pid=$(cat "$ROOT/$f")
    if kill -0 "$pid" 2>/dev/null; then
      echo "Stopping pid $pid"
      kill "$pid" || true
    fi
    rm -f "$ROOT/$f"
  fi
done

echo "Dev services stopped."

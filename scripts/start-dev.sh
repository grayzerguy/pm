#!/usr/bin/env bash
set -euo pipefail

# Start backend and frontend for local development.
# Assumes a Python virtualenv at .venv and Node/npm installed for the frontend.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT"

echo "Starting dev services using npx concurrently (falls back to background mode)..."

# Commands to run
BACKEND_CMD="$( [ -x "$ROOT/.venv/bin/python" ] && echo \"$ROOT/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend\"\" || echo \"python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend\" )"
FRONTEND_CMD="cd '$ROOT/frontend' && npm ci --silent && npm run dev"

# If npx concurrently is available (or will be downloaded), use it so logs are combined
if command -v npx >/dev/null 2>&1; then
  echo "Launching with npx concurrently to show combined logs..."
  # run concurrently in foreground so user sees logs; concurrently will auto-install if missing via npx
  npx concurrently -k -n backend,frontend -c "bgBlue.bold,bgGreen.bold" "$BACKEND_CMD" "$FRONTEND_CMD"
  exit_code=$?
  exit $exit_code
else
  # fallback: start both in background and write PIDs
  echo "npx not found — starting backend and frontend in background (PID files)"
  eval "$BACKEND_CMD &"
  BACKEND_PID=$!
  (cd "$ROOT/frontend" && npm ci --silent && npm run dev &)
  FRONTEND_PID=$!
  echo "$BACKEND_PID" > "$ROOT/.pm_backend.pid"
  echo "$FRONTEND_PID" > "$ROOT/.pm_frontend.pid"
  echo "Started dev services (background)"
  echo "- Frontend: http://localhost:3000"
  echo "- API: http://localhost:8000"
  echo "Use ./scripts/stop-dev.sh to stop both services."
  wait
fi

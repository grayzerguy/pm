# Local development (no Docker)

Use these scripts to run the frontend (Next.js dev server) and backend (uvicorn) locally without Docker.

Start both services:

```bash
./scripts/start-dev.sh
```

Stop both services:

```bash
./scripts/stop-dev.sh
```

Notes:
- `start-dev.sh` expects Node/npm installed for the frontend and a Python virtualenv at `.venv` (or will fallback to system `python`).
- Frontend dev server runs on `http://localhost:3000` and backend API on `http://localhost:8000`.

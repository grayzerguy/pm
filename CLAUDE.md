# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A single-user Kanban project management app. Next.js frontend + Python FastAPI backend, packaged into one Docker container. The backend serves the statically-exported frontend and exposes all `/api/*` routes.

Login credentials (hardcoded MVP): `user` / `password`

## Commands

### Running Locally (Docker)

```bash
./scripts/start.sh    # build image and start container at http://localhost:8000
./scripts/stop.sh     # stop and remove container
```

### Frontend Development (with live reload)

```bash
cd frontend
npm install
npm run dev           # starts Next.js dev server at :3000, proxies /api/* to :8000
npm run build         # standard Next.js build
BUILD_EXPORT=1 npm run build  # static export to frontend/out/ (used by Docker)
npm run lint
npm run test          # vitest unit tests
npm run test:e2e      # playwright e2e tests
```

Run a single test file:
```bash
cd frontend && npx vitest run src/lib/kanban.test.ts
```

### Backend Development

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest                # run all tests
```

## Architecture

### Request Flow

In **Docker/production**: Browser → FastAPI (port 8000) → serves static `frontend/out/` files for HTML/JS, handles all `/api/*` routes directly.

In **local dev**: Browser → Next.js dev server (port 3000) → rewrites `/api/*` to FastAPI (port 8000).

### Key Design Decisions

- **Static export**: Next.js is built with `BUILD_EXPORT=1` which sets `output: "export"`, producing `frontend/out/`. The Dockerfile copies this to `backend/static/` in the final image.
- **No JWT**: Auth is a simple session cookie (`session=1`) set on login, checked inline in each route handler.
- **Board storage**: SQLite at `backend/kanban.db`. Board state is stored as a single JSON blob per user in the `boards` table. `database.py` is initialized on import (auto-creates table and seeds default board for new users).
- **AI**: `backend/app/ai.py` tries OpenRouter first (`OPEN_ROUTE_API_KEY`), falls back to OpenAI (`OPENAI_API_KEY`). The `/api/chat` endpoint sends the full board JSON in the system prompt and expects the model to return a JSON object with `reply` and optionally `board_update`.

### Frontend State

`BoardData` (defined in `src/lib/kanban.ts`) is the single source of truth: `{ columns: Column[], cards: Record<string, Card> }`. It lives in React state on the root `page.tsx` and is passed down to both `KanbanBoard` and `AIChatSidebar`. Any board change triggers a `PUT /api/board` save (debounced by React's effect).

### Backend Module Map

- `app/main.py` — FastAPI app, all route handlers, SYSTEM_PROMPT for AI chat
- `app/database.py` — SQLite helpers: `init_db`, `get_board`, `save_board`
- `app/ai.py` — `call_ai(messages)` wrapping OpenRouter/OpenAI

## Color Scheme (CSS Variables)

- `--accent-yellow`: `#ecad0a`
- `--primary-blue`: `#209dd7`
- `--secondary-purple`: `#753991`
- `--navy-dark`: `#032147`
- `--gray-text`: `#888888`

## Coding Standards

- No over-engineering, no defensive programming, no extra features
- No emojis anywhere
- When hitting issues: identify root cause with evidence before fixing

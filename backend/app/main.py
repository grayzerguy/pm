from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import json
import pathlib
from app.database import init_db, get_board, save_board
from app.ai import call_ai

# --- simple auth config ----------------------------------------------------------------
VALID_USER = "user"
VALID_PASS = "password"
COOKIE_NAME = "session"
COOKIE_VALUE = "1"


def require_auth(request: Request):
    # raise 401 if no valid cookie
    if request.cookies.get(COOKIE_NAME) != COOKIE_VALUE:
        raise HTTPException(status_code=401)

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# determine where static files live; the Docker build copies the frontend export to
# `/app/static`, but when running tests locally we may build in `frontend/out` and
# copy into backend/static.  The code below tries both locations so that the same
# behaviour works in all environments.

_project_root = pathlib.Path(__file__).parent.parent
_static_dir = _project_root / "static"
_frontend_out = _project_root.parent / "frontend" / "out"


def _get_serve_dir() -> Optional[pathlib.Path]:
    if _static_dir.is_dir():
        return _static_dir
    if _frontend_out.is_dir():
        return _frontend_out
    return None


serve_dir = _get_serve_dir()

if serve_dir:
    # mount at `/static` so that assets (js/css) can be fetched.  The root
    # handler below will serve `index.html` directly.
    app.mount("/static", StaticFiles(directory=str(serve_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # redirect unauthenticated users to login page
    if request.cookies.get(COOKIE_NAME) != COOKIE_VALUE:
        return RedirectResponse(url="/login")

    sd = _get_serve_dir()
    if sd:
        index = sd / "index.html"
        if index.exists():
            return FileResponse(str(index))
    return "<html><body><h1>Hello, world!</h1></body></html>"

# catch‑all to support client‑side routing (for example when using Next's exported
# files there may be multiple html pages, but we at least want `/` to work).
@app.post("/api/login")
async def login(request: Request):
    # parse body manually rather than rely on models to keep dependencies light
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    username = payload.get("username")
    password = payload.get("password")
    if username == VALID_USER and password == VALID_PASS:
        response = {"success": True}
        # set cookie in response? Wait, for JSON, can't set cookie.
        # Need to use response object.
        from fastapi.responses import JSONResponse
        resp = JSONResponse(content=response)
        resp.set_cookie(COOKIE_NAME, COOKIE_VALUE, httponly=True)
        return resp
    raise HTTPException(status_code=401, detail="invalid credentials")


@app.post("/api/logout")
def logout():
    from fastapi.responses import JSONResponse
    resp = JSONResponse(content={"success": True})
    resp.delete_cookie(COOKIE_NAME)
    return resp


@app.get("/api/board")
def api_get_board(request: Request):
    if request.cookies.get(COOKIE_NAME) != COOKIE_VALUE:
        raise HTTPException(status_code=401)
    return get_board(VALID_USER)


@app.put("/api/board")
async def api_save_board(request: Request):
    if request.cookies.get(COOKIE_NAME) != COOKIE_VALUE:
        raise HTTPException(status_code=401)
    data = await request.json()
    save_board(VALID_USER, data)
    return {"success": True}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/ai/test")
def ai_test(request: Request):
    require_auth(request)
    try:
        answer = call_ai([{"role": "user", "content": "What is 2+2? Reply with just the number."}])
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    board: Dict[str, Any]


SYSTEM_PROMPT = """You are an AI assistant helping manage a Kanban project board.

The current board state is provided below as JSON. When the user asks you to create, move, or edit cards, update the board and return the full new board state.

Board structure:
- columns: list of {{id, title, cardIds}}
- cards: dict mapping card_id -> {{id, title, details}}
- Default column IDs: col-backlog, col-discovery, col-progress, col-review, col-done
- For new cards generate a unique id like "card-" followed by a short random string

Always respond with a JSON object and nothing else (no markdown fences):
{{
  "reply": "friendly message describing what you did or answering the question",
  "board_update": null
}}

OR if the board changed:
{{
  "reply": "friendly message describing the changes",
  "board_update": {{...complete updated board...}}
}}

Current board:
{board_json}"""


@app.post("/api/chat")
async def api_chat(request: Request, body: ChatRequest):
    require_auth(request)
    system = SYSTEM_PROMPT.format(board_json=json.dumps(body.board, ensure_ascii=False))
    messages = [{"role": "system", "content": system}]
    messages += [{"role": m.role, "content": m.content} for m in body.messages]
    try:
        raw = call_ai(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # parse structured response
    try:
        # strip possible markdown fences the model may add despite instructions
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)
    except Exception:
        # fallback: treat raw text as a plain reply with no board update
        result = {"reply": raw, "board_update": None}

    board_update = result.get("board_update")
    if board_update:
        save_board(VALID_USER, board_update)

    return {"reply": result.get("reply", ""), "board_update": board_update}


# catch‑all to support client‑side routing (for example when using Next's exported
# files there may be multiple html pages, but we at least want `/` to work)
# We need to make sure any API routes are defined before this handler or we
# explicitly ignore the `/api` prefix here, otherwise all requests under `/api`
# will be swallowed by the wildcard.
@app.get("/{full_path:path}", response_class=HTMLResponse)
def catch_all(full_path: str, request: Request):
    # don't intercept API requests
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404)
    # always serve static assets without auth check
    if full_path.startswith("_next/") or full_path.startswith("static/"):
        sd = _get_serve_dir()
        if sd:
            candidate = sd / full_path
            if candidate.is_file():
                return FileResponse(str(candidate))
        raise HTTPException(status_code=404)
    # if the user is not logged in and is not heading to login page, redirect
    if request.cookies.get(COOKIE_NAME) != COOKIE_VALUE and not full_path.startswith("login"):
        return RedirectResponse(url="/login")
    sd = _get_serve_dir()
    if sd:
        # try serving a file/directory that matches the requested path
        candidate = sd / full_path
        # check for directory with index.html
        if candidate.is_dir():
            index = candidate / "index.html"
            if index.exists():
                return FileResponse(str(index))
        # check for exact file (including .html extension)
        if candidate.is_file():
            return FileResponse(str(candidate))
        html_file = sd / f"{full_path}.html"
        if html_file.is_file():
            return FileResponse(str(html_file))
        # fall back to root index for client-side routes
        index = sd / "index.html"
        if index.exists():
            return FileResponse(str(index))
    raise HTTPException(status_code=404)

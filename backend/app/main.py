from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pathlib

app = FastAPI()

# determine where static files live; the Docker build copies the frontend export to
# `/app/static`, but when running tests locally we may build in `frontend/out` and
# copy into backend/static.  The code below tries both locations so that the same
# behaviour works in all environments.

_project_root = pathlib.Path(__file__).parent.parent
_static_dir = _project_root / "static"
_frontend_out = _project_root.parent / "frontend" / "out"

# prefer the explicit static directory if it exists, otherwise fall back to the
# exported frontend output (used during development when tests build the site).
if _static_dir.is_dir():
    serve_dir = _static_dir
elif _frontend_out.is_dir():
    serve_dir = _frontend_out
else:
    serve_dir = None

if serve_dir:
    # mount at `/static` so that assets (js/css) can be fetched.  The root
    # handler below will serve `index.html` directly.
    app.mount("/static", StaticFiles(directory=str(serve_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    if serve_dir:
        index = serve_dir / "index.html"
        if index.exists():
            return FileResponse(str(index))
    return "<html><body><h1>Hello, world!</h1></body></html>"

# catch‑all to support client‑side routing (for example when using Next's exported
# files there may be multiple html pages, but we at least want `/` to work).
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# catch‑all to support client‑side routing (for example when using Next's exported
# files there may be multiple html pages, but we at least want `/` to work)
# We need to make sure any API routes are defined before this handler or we
# explicitly ignore the `/api` prefix here, otherwise all requests under `/api`
# will be swallowed by the wildcard.
@app.get("/{full_path:path}", response_class=HTMLResponse)
def catch_all(full_path: str):
    # don't intercept API requests
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404)
    if serve_dir:
        index = serve_dir / "index.html"
        if index.exists():
            return FileResponse(str(index))
    raise HTTPException(status_code=404)

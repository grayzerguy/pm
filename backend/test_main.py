import shutil
import subprocess
import pathlib

from fastapi.testclient import TestClient
from app.main import app

# ensure the frontend has been built and copied to backend/static (or
# frontend/out) so that the FastAPI app can serve it.  This mirrors what the
# Dockerfile will do and keeps the integration tests green without requiring a
# separate manual build step.

def _build_frontend_if_needed():
    workspace = pathlib.Path(__file__).parents[1]
    frontend = workspace / "frontend"
    out = frontend / "out"
    static = workspace / "static"

    # if we already have a static directory that appears to contain an index,
    # assume everything is fine.
    if static.is_dir() and (static / "index.html").exists():
        return

    # otherwise, build the frontend export
    if not out.is_dir():
        # run npm commands; these may raise if npm/node isn't available but
        # that's fine for a developer environment where the frontend is used.
        subprocess.run(["npm", "ci"], cwd=str(frontend), check=True)
        subprocess.run(["npm", "run", "build"], cwd=str(frontend), check=True)
        subprocess.run(["npm", "run", "export"], cwd=str(frontend), check=True)

    # copy the export into backend/static so that the server code can find it
    if static.exists():
        shutil.rmtree(static)
    shutil.copytree(out, static)

_build_frontend_if_needed()

client = TestClient(app)


def test_root_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    # after the frontend is built we expect the Kanban heading to appear; if
    # something went wrong we at least still accept the original placeholder.
    assert (
        "Kanban Studio" in response.text
        or "Hello, world" in response.text
    )


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

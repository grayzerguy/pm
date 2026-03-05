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

    # always rebuild so that new pages (e.g. login) are picked up.  This
    # keeps tests deterministic and avoids stale exports lingering in CI.
    if static.is_dir():
        shutil.rmtree(static)

    # otherwise, build the frontend export
    # rebuild output unconditionally so new routes/pages show up
    if out.is_dir():
        shutil.rmtree(out)
    # run npm commands; these may raise if npm/node isn't available but
    # that's fine for a developer environment where the frontend is used.
    subprocess.run(["npm", "ci"], cwd=str(frontend), check=True)
    subprocess.run(["npm", "run", "build"], cwd=str(frontend), check=True, env={**__import__("os").environ, "BUILD_EXPORT": "1"})
    # next export is not needed since we build with `output: 'export'` in
    # next.config.ts; `next build` already produces the out/ directory.

    # copy the export into backend/static so that the server code can find it
    if static.exists():
        shutil.rmtree(static)
    shutil.copytree(out, static)

_build_frontend_if_needed()

client = TestClient(app)


def test_root_returns_html():
    client.cookies.clear()
    # authenticated request should return the page
    response = client.post(
        "/api/login",
        json={"username": "user", "password": "password"},
    )
    # cookie is stored on the client object
    cookie = client.cookies.get("session")
    assert cookie == "1"

    response = client.get("/")
    assert response.status_code == 200
    assert (
        "Kanban Studio" in response.text
        or "Hello, world" in response.text
    )


def test_root_redirects_when_unauthenticated():
    client.cookies.clear()
    resp = client.get("/")
    # without auth cookie we should be on login page
    assert resp.status_code == 200
    assert "<form" in resp.text or "Log in" in resp.text


def test_login_logout_flow():
    # invalid credentials
    resp = client.post("/api/login", json={"username": "foo", "password": "bar"})
    assert resp.status_code == 401

    # valid credentials
    client.cookies.clear()
    resp = client.post(
        "/api/login",
        json={"username": "user", "password": "password"},
    )
    session = client.cookies.get("session")
    assert session == "1"

    # logout returns JSON success and clears cookie
    resp2 = client.post("/api/logout")
    assert resp2.status_code == 200
    assert resp2.json() == {"success": True}
    # cookie should no longer be present
    assert client.cookies.get("session") in (None, "")


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_board_get_requires_auth():
    client.cookies.clear()
    resp = client.get("/api/board")
    assert resp.status_code == 401


def test_board_get_returns_data():
    client.cookies.clear()
    client.post("/api/login", json={"username": "user", "password": "password"})
    resp = client.get("/api/board")
    assert resp.status_code == 200
    data = resp.json()
    assert "columns" in data
    assert "cards" in data
    assert len(data["columns"]) == 5


def test_board_save_and_reload():
    client.cookies.clear()
    client.post("/api/login", json={"username": "user", "password": "password"})
    original = client.get("/api/board").json()
    # rename first column
    original["columns"][0]["title"] = "Modified"
    resp = client.put("/api/board", json=original)
    assert resp.status_code == 200
    reloaded = client.get("/api/board").json()
    assert reloaded["columns"][0]["title"] == "Modified"
    # restore original title
    reloaded["columns"][0]["title"] = "Backlog"
    client.put("/api/board", json=reloaded)

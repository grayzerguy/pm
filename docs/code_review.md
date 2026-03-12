# Code Review

Reviewed: all backend Python, all frontend TypeScript/TSX, Dockerfile, test files, and supporting config.

Issues are grouped by severity. Each has a file reference and a concrete recommended action.

---

## Critical

### 1. Real API keys committed to git — `.env`

The `.env` file in the project root contains live `OPENAI_API_KEY` and `OPEN_ROUTE_API_KEY` values and is tracked by git (not in `.gitignore`). Anyone with access to the repository history can read these keys.

**Action:** Add `.env` to `.gitignore`, add a `.env.example` with placeholder values, and rotate both keys immediately.

---

## High

### 2. Board saves are fire-and-forget — `KanbanBoard.tsx:33`

The `useEffect` that saves board state on every change does:
```ts
fetch("/api/board", { method: "PUT", ... });
```
The returned Promise is not awaited and errors are silently swallowed. If a save fails (network error, 401 timeout), the user has no indication and their changes are lost on refresh.

**Action:** Await the fetch and show an error indicator on failure, or at minimum log to console. A simple `catch(console.error)` is the minimum fix.

### 3. Column rename fires an API save on every keystroke — `KanbanColumn.tsx:46`, `KanbanBoard.tsx:27`

The column title `<input>` calls `onRename` on every `onChange`, which updates board state, which triggers the save `useEffect`. A user renaming "Backlog" to "Releases" sends 7 PUT requests in sequence.

**Action:** Debounce the save effect (e.g. 500ms), or switch the column rename to save only on `onBlur`.

### 4. Backend test suite rebuilds the entire frontend unconditionally — `test_main.py:14–41`

`_build_frontend_if_needed()` runs `npm ci` and `npm run build` every time the test suite is invoked, regardless of whether sources changed. This is why `pytest` takes 65 seconds. The comment acknowledges it is always rebuilt by design, but this makes iterating on backend tests painful.

**Action:** Check a hash or mtime of the source files, or only rebuild when `frontend/src/**` is newer than `backend/static/`. Alternatively, add a `--no-rebuild` flag via an environment variable so developers can skip the rebuild when they know static files are current.

### 5. `init_db()` is called twice at startup — `database.py:70`, `main.py:26`

`database.py` calls `init_db()` at the bottom of the module (line 70) so the table exists on import. `main.py` also calls `init_db()` in the `lifespan` handler. On every startup the function runs twice. While `CREATE TABLE IF NOT EXISTS` makes it idempotent, it is confusing.

**Action:** Remove the bare `init_db()` call at the bottom of `database.py` — the `lifespan` call in `main.py` is the correct place for startup initialization.

---

## Medium

### 6. `JSONResponse` imported twice inside function bodies — `main.py:84,94`

`JSONResponse` is already imported at the top of `main.py` but is re-imported inside both `login()` and `logout()`:
```python
from fastapi.responses import JSONResponse
resp = JSONResponse(content=...)
```

**Action:** Remove the two inner import statements. The top-level import is sufficient.

### 7. `__import__()` used inline instead of top-level imports — `test_main.py:32,176`

`test_main.py` uses `__import__("os").environ` and `__import__("json").dumps(...)`. These are obscure and hard to read.

**Action:** Add `import os` and `import json` at the top of the file and use them directly.

### 8. Auth check is inconsistent across routes — `main.py`

There are three different patterns for the same check:
- `require_auth(request)` helper (used in `/api/ai/test`, `/api/chat`)
- Inline `if request.cookies.get(COOKIE_NAME) != COOKIE_VALUE: raise HTTPException(status_code=401)` (used in `GET /api/board`, `PUT /api/board`)
- Inline check with redirect (used in `GET /`)

**Action:** Use `require_auth` consistently for all API routes. The redirect behaviour for the root HTML route is intentionally different and can stay as-is.

### 9. No error state for board loading — `page.tsx:14–29`

If the initial `GET /api/board` fetch throws a network error (not a 401), the component stays in the "Loading..." state forever with no user-visible error.

**Action:** Add a `try/catch` around the fetch and show an error message if it fails.

### 10. Login form: no loading state, labels not linked to inputs — `login/page.tsx`

Two issues:
- The submit button has no `disabled` state while a request is in flight, so double-submitting is possible.
- The `<label>` elements are not associated with their inputs (no `htmlFor`/`id` pairing). Screen readers cannot associate them.

**Action:** Add a `loading` state boolean to disable the button during submission. Add matching `htmlFor` on labels and `id` on inputs.

### 11. Logout button uses hardcoded Tailwind color, not design system — `KanbanBoard.tsx:148`

```tsx
className="... bg-red-500 ..."
```
All other interactive elements use CSS variable-based colors from the design system. The logout button is the sole exception.

**Action:** Replace `bg-red-500` with a design system color (e.g. `bg-[var(--secondary-purple)]`) or define a `--danger` CSS variable.

### 12. `AIChatSidebar` `setBoard` prop type is too narrow — `AIChatSidebar.tsx:13`

The prop is typed as `setBoard: (board: BoardData) => void` but the actual value passed from `page.tsx` is `React.Dispatch<React.SetStateAction<BoardData>>`, which also accepts an updater function `(prev) => newBoard`. The narrower type is technically compatible but hides the full capability and is inconsistent with `KanbanBoard`'s prop type.

**Action:** Change the `AIChatSidebar` prop type to `React.Dispatch<React.SetStateAction<BoardData>>` to match `KanbanBoard`.

---

## Low

### 13. `handleDragStart` and `handleDragEnd` are not memoized — `KanbanBoard.tsx:49,53`

`handleRenameColumn`, `handleAddCard`, and `handleDeleteCard` all use `useCallback`. `handleDragStart` and `handleDragEnd` are defined inline without `useCallback`, recreating them on every render. Inconsistent pattern.

**Action:** Wrap `handleDragStart` and `handleDragEnd` in `useCallback` for consistency. Impact on performance is negligible but maintains the established pattern.

### 14. `SYSTEM_PROMPT.format()` is fragile with user-provided board JSON — `main.py:140–163`

The system prompt uses Python's `.format(board_json=...)` to embed the board state. If a card title or details field contains the literal string `{board_json}` or any other `{word}` pattern, `str.format()` will raise a `KeyError`.

**Action:** Use `SYSTEM_PROMPT.replace("{board_json}", board_json_str)` or use `%` formatting (`... %s % board_json_str`) to avoid `.format()` interpreting brace patterns inside user content. Alternatively, split the prompt so the board JSON is appended as a separate string rather than interpolated.

### 15. `call_ai` only catches `HTTPStatusError`, not network errors — `ai.py:22–26`

The fallback from OpenRouter to OpenAI only triggers on `HTTPStatusError` with status 401/402/403. If OpenRouter is unreachable (DNS failure, timeout), the exception propagates to the route handler as an unhandled `ConnectError` or `TimeoutException`.

**Action:** Catch `httpx.TransportError` (the base class for network-level errors) in the fallback logic, or document that network errors propagate as 500 to the client (which they currently do, implicitly).

### 16. AI chat history is lost on page refresh — `AIChatSidebar.tsx`

The conversation `messages` array is held in local component state only. Refreshing the page or navigating away clears the entire chat history.

**Action:** This is tracked in `docs/FUTURE.md` already. No action needed for MVP — just confirming it is a known limitation and not an oversight.

### 17. Dockerfile uses `pip` instead of `uv` — `Dockerfile:21`

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
The project AGENTS.md specifies `uv` as the Python package manager for Docker. The Dockerfile uses `pip` instead.

**Action:** Replace with `uv` if consistency with the stated technical decisions matters:
```dockerfile
RUN pip install uv && uv pip install --system -r requirements.txt
```
Or update AGENTS.md to reflect that `pip` is used in Docker. Either is fine — just resolve the inconsistency.

---

## Summary table

| # | Severity | Area | One-line description |
|---|----------|------|----------------------|
| 1 | Critical | Security | Real API keys in git-tracked `.env` |
| 2 | High | Frontend | Board save errors silently swallowed |
| 3 | High | Frontend | Column rename fires API call on every keystroke |
| 4 | High | Tests | Frontend rebuilt unconditionally on every test run |
| 5 | High | Backend | `init_db()` called twice at startup |
| 6 | Medium | Backend | `JSONResponse` re-imported inside function bodies |
| 7 | Medium | Tests | `__import__()` used instead of top-level imports |
| 8 | Medium | Backend | Auth check pattern inconsistent across routes |
| 9 | Medium | Frontend | No error state for board loading failure |
| 10 | Medium | Frontend | Login form: no loading state, inaccessible labels |
| 11 | Medium | Frontend | Logout button breaks design system color convention |
| 12 | Medium | Frontend | `AIChatSidebar.setBoard` prop type too narrow |
| 13 | Low | Frontend | `handleDragStart`/`handleDragEnd` not memoized |
| 14 | Low | Backend | `SYSTEM_PROMPT.format()` fragile with user content |
| 15 | Low | Backend | `call_ai` does not catch network-level errors |
| 16 | Low | Frontend | Chat history lost on refresh (known/tracked) |
| 17 | Low | Infra | Dockerfile uses `pip`, AGENTS.md specifies `uv` |

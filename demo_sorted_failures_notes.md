# Building demo_sorted_failures.py

Date: 2026-10-15

## Goal
Show that `ask()` in `sorted_failures_class.py` catches and logs each kind of failure correctly.

## Approach
`demo_sorted_failures.py` swaps `sf.client` and `sf.MODEL` per case (restored at the end), calls `sf.ask()`, and checks that the expected exception is raised.

| Case | Trigger | Expected |
|---|---|---|
| success | normal call | returns response |
| 400 | empty `messages` | `BadRequestError` |
| 401 | fake API key | `AuthenticationError` |
| 404 | nonexistent model | `APIStatusError` (`NotFoundError`) |
| 429 | mocked HTTP response | `RateLimitError` |
| 500 | mocked HTTP response | `InternalServerError` (via `APIStatusError`) |
| connection | `base_url` on a dead port | `APIConnectionError` |
| truncation | real call, `max_tokens=5` | `TruncatedOutput` |
| refusal | mocked `stop_reason: "refusal"` | `RuntimeError` |

Real API calls: success, 400, 401, 404, truncation (about 50 tokens billed in total). Everything else is offline.

## Issues hit
- `ModuleNotFoundError: No module named 'httpx'`. The venv has `anthropic 1.13.0`, which depends on `httpx2` and rejects plain `httpx` clients. Fix: `try: import httpx2 as httpx` with a fallback to `httpx`.
- Demo clients use `max_retries=0` so failures show immediately. The real client uses `max_retries=3`, which would retry 429, 5xx and connection errors with backoff before raising.

## Result
All 9 cases PASS.

Run: `venv\Scripts\python.exe demo_sorted_failures.py`

## Side questions in the same session
- `claude -p` needs a prompt as an argument or on stdin (for example `claude -p "..."` or `"..." | claude -p`).
- `/memory` is an interactive slash command. Type it in a `claude` session or in the VS Code chat box. It does not work with `-p`.

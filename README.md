# UI Tests (Playwright + Pytest + POM)

Covers Login, Signup, and Users Table pages on `http://localhost:5173` with:
- Python + Pytest + Playwright
- Page Object Model (POM)
- Django-style logging (via `logging.config.dictConfig`)
- Parallel execution (pytest-xdist) across **all browsers** (Chromium, Firefox, WebKit)
- Dockerized execution (runs browsers headless in container)
- Rich fixtures: login/logout, per-user storage state, session duration manipulation (time travel), multi-browser matrix
- Docstrings throughout

## Prereqs
- Python 3.11+
- Docker (optional, for containerized run)

## Install & Run (local machine)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
playwright install --with-deps
cp .env.example .env  # adjust BASE_URL if needed
pytest -n auto -q
```

### All browsers at once
Tests are parametrized to run across `chromium`, `firefox`, and `webkit` automatically.

### Credentials
- regular: `test1 / megaboss19`
- regular: `test28 / megaboss19`
- admin:   `admin / changeme123`

## Run in Docker
### macOS/Windows (host is accessible as `host.docker.internal`)
```bash
docker compose run --rm tests
```

### Linux (prefer host networking so tests can reach `localhost:5173`)
```bash
docker compose -f docker-compose.yml -f docker-compose.linux.yml run --rm tests
```
If you cannot use host networking, set `BASE_URL=http://host.docker.internal:5173` and expose your app to the container.

## Useful invocations
```bash
# only login tests
pytest tests/test_login.py -n auto -q

# debug a single test in headed mode
PWDEBUG=1 pytest -k test_login_success --browser=chromium -q

# record video & traces
pytest --video=on --tracing=on -n auto -q
```

## Config via env
| Var | Default | Notes |
|-----|---------|-------|
| `BASE_URL` | `http://localhost:5173` | Point to your app |
| `SESSION_MINUTES` | `30` | Logical session duration used by time-travel helper |
| `HEADLESS` | `1` | Set `0` to see browsers locally |

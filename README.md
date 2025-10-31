# !!! THE PROJECT IS UNDER DEVELOPMENT!!!


### QA Framework (Playwright + Pytest + Django)

See `pytest.ini`, `playwright.config.ts`, and tests under `tests/`.
Run:
```bash
playwright install --with-deps
pip install -e .
pytest -n auto --all-browsers
```
Docker:
```bash
docker compose up --build --abort-on-container-exit
```
Adjust selectors if your DOM differs.

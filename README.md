# UI QA Automation Framework (Playwright + Pytest + Django logging)

This is a production-grade, **parallel** UI automation framework targeting the provided app.

## Tech
- Python 3.11+
- Playwright (sync API)
- Pytest (+ xdist for parallelism, HTML report plugin)
- Page Object Model (per page file) with docstrings
- Django logging via Loguru (collected to `logs/`)
- Test data generation via the UI Excel Import
- Multi-browser runs (Chromium, Firefox, WebKit) in one go
- Dark/Light theme & i18n checks
- Multi-column sorting checks (stable tiebreaker aware)

## Quick start

1) **Install deps**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps
```

2) Ensure the app is running locally (frontend at `http://localhost:5173/login` and backend per the repo).

3) **Run the full, multi-browser suite in parallel**:
```bash
pytest -n auto --html=report.html --self-contained-html
```

By default the framework runs **all three browsers** (Chromium, Firefox, WebKit) concurrently via parametrized fixtures. You can scope to one browser with, e.g.:
```bash
pytest -k login --browser-list=chromium
```

4) Open `report.html` and the `logs/` folder for details.

### Useful options
- `--base-url`: override base URL (default: `http://localhost:5173`)
- `--browser-list`: comma-separated browsers, default: `chromium,firefox,webkit`
- `--headed`: run headed (default: headless)
- `--video`: record video (on|off), default: off
- `--trace`: record Playwright trace (on|off), default: off

## Structure
```
qa_framework/
  requirements.txt
  pytest.ini
  README.md
  tests/
    conftest.py
    utils/
      config.py
      logger.py
      api.py
      excel.py
    pages/
      base_page.py
      components/
        navbar.py
      login_page.py
      users_page.py
      settings_page.py
      excel_import_page.py
      stats_page.py
      profile_edit_page.py
      profile_view_page.py
      change_password_page.py
      reset_password_page.py
      signup_page.py
      user_delete_confirm_page.py
    test_login_page.py
    test_users_page.py
    test_settings_page.py
    test_i18n_and_theme.py
    test_excel_import_and_sorting.py
```

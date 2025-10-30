# Users App – E2E Test Framework

This repository contains a **Playwright + Pytest** end‑to‑end suite for the Users App (Django REST + React). It follows **POM**, runs **all browsers in parallel**, and includes fixtures for **login/logout**, **session settings override**, **theme** and **localization** checks, and **multi‑column sorting** with **Excel import** seeding.

## Quick start

1. Copy `.env.example` to `.env` and adjust if needed.
2. Install deps and Playwright browsers + run tests:
   ```bash
   ./scripts/run_all.sh
   ```

## Structure

- `tests/pages/*` — Page Objects (Login, Users, Settings, Profile, Excel Import, Navbar)
- `tests/test_*.py` — Tests grouped by page
- `tests/utils/*` — Config and logging (Django‑style)
- `config/*` — Centralized YAML config + logging
- `scripts/*` — Helper run scripts

## Notes

- **All browsers at once:** set `BROWSERS=chromium,firefox,webkit` (default).
- **Parallel:** enabled via `pytest -n auto` and session-scoped browser parametrization.
- **Django logging:** logging configured in `config/logging.yaml` with a rotating file handler.
- **Theme/i18n:** theme toggled via dedicated button; locale switched by setting `localStorage.i18nextLng`.
- **Multi-column sort:** seeds deterministic users via Excel import and validates combined sort orders.

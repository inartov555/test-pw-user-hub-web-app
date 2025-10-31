"""Global pytest configuration, Playwright bootstrapping, and cross-cutting fixtures.

- Spins up playwright browsers per --all-browsers
- Manages auth (login/logout), theme, locale, session duration
- Exposes Page Objects
- Seeds data for sorting tests via Django or Admin UI
"""
from __future__ import annotations
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

from playwright.sync_api import Playwright, sync_playwright

from tests.fixtures.browser_matrix import BROWSERS
from tests.fixtures.auth_fixtures import login, logout
from tests.fixtures.theme_locale_fixtures import set_theme, set_locale
from tests.fixtures.session_fixtures import set_session_duration
from tests.fixtures.data_seed_fixtures import ensure_sorting_data

from tests.pages.login_page import LoginPage
from tests.pages.dashboard_page import DashboardPage
from tests.pages.users_page import UsersPage
from tests.pages.settings_page import SettingsPage

BASE_URL = os.getenv("BASE_URL", "http://localhost:5173")

@pytest.fixture(scope="session")
def playwright_contexts(request):
    """Create playwright browser contexts for all requested browsers.

    Returns a mapping {browser_name: (browser, context)} for reuse via per-test pages.
    """
    browsers = request.config.getoption("--all-browsers") and BROWSERS or ["chromium"]
    instances = {}
    with sync_playwright() as pw:
        for name in browsers:
            browser = getattr(pw, name).launch(headless=not request.config.getoption("--headed"))
            context = browser.new_context(base_url=BASE_URL)
            instances[name] = (browser, context)
        yield instances
        for _, (browser, _) in instances.items():
            browser.close()

@pytest.fixture()
def page(playwright_contexts, request):
    """Provide a fresh page for the selected browser (param `browser_name`)."""
    browser_name = getattr(request, 'param', None) or request.node.funcargs.get('browser_name', 'chromium')
    _, context = playwright_contexts[browser_name]
    page = context.new_page()
    yield page
    page.close()

# Page object fixtures
@pytest.fixture()
def login_page(page):
    return LoginPage(page)

@pytest.fixture()
def dashboard_page(page):
    return DashboardPage(page)

@pytest.fixture()
def users_page(page):
    return UsersPage(page)

@pytest.fixture()
def settings_page(page):
    return SettingsPage(page)

# Cross-cutting setup/teardown
@pytest.fixture(autouse=True)
def _session_setup_teardown(request, page):
    """Auto apply: set locale/theme/session before each test and logout after.

    Per-test overrides via markers: theme(name), locale(name), session(minutes)
    """
    theme = request.node.get_closest_marker("theme")
    locale = request.node.get_closest_marker("i18n")
    session = request.node.get_closest_marker("session")

    set_locale(page, (locale and locale.kwargs.get("name")) or os.getenv("DEFAULT_LOCALE", "en"))
    set_theme(page, (theme and theme.kwargs.get("name")) or os.getenv("DEFAULT_THEME", "light"))
    set_session_duration(page, int((session and session.kwargs.get("minutes")) or os.getenv("DEFAULT_SESSION_MINUTES", 30)))

    yield

    try:
        logout(page)
    except Exception:
        pass

@pytest.fixture(scope="session", autouse=True)
def _seed_sorting_data():
    """Ensure sorting dataset exists exactly once per session."""
    ensure_sorting_data()

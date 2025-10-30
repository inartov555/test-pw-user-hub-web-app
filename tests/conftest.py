"""Pytest fixtures for Playwright + app helpers.

- Parametrize browsers from config to allow running all at once.
- Provide login fixtures for admin and users.
- Provide session settings override (with automatic revert).
- Enable parallel-safe context creation.
"""
from __future__ import annotations
import os, json, pytest, time
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, expect
from .utils.config import load_settings
from .utils.logger import logger
from .pages.login_page import LoginPage
from .pages.navbar import Navbar
from .pages.settings_page import SettingsPage

settings = load_settings()

def pytest_addoption(parser):
    parser.addoption("--browsers", action="store", default=",".join(settings.browsers), help="Comma list of browsers: chromium,firefox,webkit")
    parser.addoption("--base-url", action="store", default=settings.base_url, help="Base URL of the app")

def browser_param_list(config) -> list[str]:
    opt = config.getoption("--browsers")
    items = [x.strip() for x in opt.split(",") if x.strip()]
    valid = {"chromium","firefox","webkit"}
    out = [x for x in items if x in valid]
    return out or ["chromium"]

@pytest.fixture(params=lambda config: browser_param_list(config), scope="session")
def browser_name(request):
    """Param of browser name for session scope."""
    return request.param

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright, browser_name):
    logger.info(f"Launching browser: {browser_name}")
    browser = getattr(playwright, browser_name).launch(headless=settings.headless, slow_mo=settings.slowmo_ms)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    ctx = browser.new_context(locale=settings.default_locale, viewport={"width":1280,"height":800})
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext, request) -> Page:
    base = request.config.getoption("--base-url")
    p = context.new_page()
    p.set_default_timeout(10000)
    p.set_default_navigation_timeout(15000)
    # Always start on base URL so SPA has router
    p.goto(base)
    return p

@pytest.fixture(scope="function")
def login_admin(page: Page):
    lp = LoginPage(page, settings.base_url)
    lp.open()
    lp.login(os.getenv("ADMIN_USER","admin"), os.getenv("ADMIN_PASS","changeme123"))
    # Expect Users tab visible
    expect(page.get_by_role("link", name="Users")).to_be_visible()
    return page

@pytest.fixture(scope="function")
def login_user1(page: Page):
    lp = LoginPage(page, settings.base_url)
    lp.open()
    lp.login(os.getenv("USER1","test1"), os.getenv("USER1_PASS","megaboss19"))
    expect(page.get_by_role("link", name="Profile")).to_be_visible()
    return page

@pytest.fixture(scope="function")
def logout(page: Page):
    nb = Navbar(page, settings.base_url)
    yield
    try:
        nb.logout()
    except Exception:
        pass

@pytest.fixture(scope="function")
def override_session_settings(login_admin: Page):
    """Temporarily adjust auth settings; restore after."""
    nb = Navbar(login_admin, settings.base_url)
    nb.toggle_additional()
    nb.nav_to("Settings")
    sp = SettingsPage(login_admin, settings.base_url)
    sp.open()
    orig = sp.read_current_values()
    sp.set_auth_values(renew=300, idle=600, lifetime=900)
    sp.save()
    yield
    # restore
    sp.set_auth_values(*orig)
    sp.save()

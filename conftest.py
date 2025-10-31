"""
pytest configuration & Playwright fixtures for E2E tests.
"""

from __future__ import annotations
import pathlib
from typing import Generator

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from config.settings import settings
from utils.time_travel import install_time_travel, advance_minutes
from utils.test_data import USERS
from pages.login_page import LoginPage


ARTIFACTS = pathlib.Path(".artifacts")
ARTIFACTS.mkdir(exist_ok=True)

BROWSERS = ("chromium", "firefox", "webkit")

STATE_DIR = ARTIFACTS / "storage"
STATE_DIR.mkdir(parents=True, exist_ok=True)


def _launch(pw, name: str) -> Browser:
    """
    Launch a browser engine by name with the configured headless setting.
    """
    headless = settings.headless
    if name == "chromium":
        return pw.chromium.launch(headless=headless)
    if name == "firefox":
        return pw.firefox.launch(headless=headless)
    if name == "webkit":
        return pw.webkit.launch(headless=headless)
    raise ValueError(name)


@pytest.fixture(name="browser", params=BROWSERS, scope="session")
def browser_fixture(request) -> Generator[Browser, None, None]:
    """
    Session-scoped Playwright Browser for each engine (runs in parallel with xdist).
    """
    with sync_playwright() as pw:
        br = _launch(pw, request.param)
        yield br
        br.close()


@pytest.fixture(name="context")
def context_fixture(browser: Browser, request) -> Generator[BrowserContext, None, None]:
    """
    Fresh BrowserContext per test for isolation and video capture.
    """
    ctx = browser.new_context(record_video_dir=str(ARTIFACTS / "videos"))
    yield ctx
    ctx.close()


@pytest.fixture(name="page")
def page_fixture(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Blank Playwright Page with time-travel shim installed.
    """
    page = context.new_page()
    install_time_travel(page)
    yield page


@pytest.fixture(name="base_url", scope="session")
def base_url_fixture() -> str:
    """
    Application base URL under test (stripped of trailing slash).
    """
    return settings.base_url.rstrip("/")


def _state_file(username: str) -> pathlib.Path:
    """
    Return the path to the persisted storage state file for a username.
    """
    return STATE_DIR / f"{username}.json"


def _perform_login(page: Page, base_url: str, username: str, password: str) -> None:
    """
    Log in via the UI and leave the authenticated state in the context.
    """
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login(username, password)


@pytest.fixture(name="storage_state_regular1", scope="session")
def storage_state_regular1_fixture(browser: Browser, base_url: str) -> str:
    """
    Create/reuse persisted storage state for regular1 and return its file path.
    """
    state = _state_file("test1")
    if not state.exists():
      ctx = browser.new_context()
      p = ctx.new_page()
      _perform_login(p, base_url, USERS["regular1"]["username"], USERS["regular1"]["password"])
      ctx.storage_state(path=str(state))
      ctx.close()
    return str(state)


@pytest.fixture(scope="session")
def storage_state_regular2(browser: Browser, base_url: str) -> str:
    """
    Create/reuse persisted storage state for regular2 and return its file path.
    """
    state = _state_file("test28")
    if not state.exists():
        ctx = browser.new_context()
        p = ctx.new_page()
        _perform_login(p, base_url, USERS["regular2"]["username"], USERS["regular2"]["password"])
        ctx.storage_state(path=str(state))
        ctx.close()
    return str(state)


@pytest.fixture(name="storage_state_admin", scope="session")
def storage_state_admin_fixture(browser: Browser, base_url: str) -> str:
    """
    Create/reuse persisted storage state for admin and return its file path.
    """
    state = _state_file("admin")
    if not state.exists():
        ctx = browser.new_context()
        p = ctx.new_page()
        _perform_login(p, base_url, USERS["admin"]["username"], USERS["admin"]["password"])
        ctx.storage_state(path=str(state))
        ctx.close()
    return str(state)


@pytest.fixture()
def logged_in_regular1(browser: Browser, storage_state_regular1: str) -> Generator[Page, None, None]:
    """
    Provide a Page already authenticated as regular1.
    """
    ctx = browser.new_context(storage_state=storage_state_regular1)
    page = ctx.new_page()
    install_time_travel(page)
    yield page
    ctx.close()


@pytest.fixture()
def logged_in_admin(browser: Browser, storage_state_admin: str) -> Generator[Page, None, None]:
    """
    Provide a Page already authenticated as admin.
    """
    ctx = browser.new_context(storage_state=storage_state_admin)
    page = ctx.new_page()
    install_time_travel(page)
    yield page
    ctx.close()


@pytest.fixture()
def expire_session(page: Page):
    """
    Advance logical time beyond SESSION_MINUTES to force auth expiry.
    """
    def _go():
        advance_minutes(page, settings.session_minutes + 1)
    return _go


@pytest.fixture()
def logout(page: Page):
    """
    UI logout via the header component, ignoring missing controls.
    """
    from pages.base_page import BasePage
    b = BasePage(page)
    def _go():
        try:
            b.header().logout()
        except TimeoutError:
            pass
    return _go

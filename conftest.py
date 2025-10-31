"""
conftest.py
"""

from __future__ import annotations
import os
import pathlib
import pytest
from typing import Generator

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
    Session-scoped browser for each engine; all three in parallel via xdist.
    """
    with sync_playwright() as pw:
        br = _launch(pw, request.param)
        yield br
        br.close()


@pytest.fixture(name="context")
def context_fixture(browser: Browser, request) -> Generator[BrowserContext, None, None]:
    """
    Fresh context per test to ensure isolation.
    """
    ctx = browser.new_context(record_video_dir=str(ARTIFACTS / "videos"))
    yield ctx
    ctx.close()


@pytest.fixture(name="page")
def page_fixture(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Getting a new page
    """
    page = context.new_page()
    install_time_travel(page)
    yield page


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Base URL under test.
    """
    return settings.base_url.rstrip("/")


def _state_file(username: str) -> pathlib.Path:
    return STATE_DIR / f"{username}.json"


def _perform_login(page: Page, base_url: str, username: str, password: str) -> None:
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login(username, password)


@pytest.fixture(scope="session")
def storage_state_regular1(browser: Browser, base_url: str) -> str:
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
    state = _state_file("test28")
    if not state.exists():
        ctx = browser.new_context()
        p = ctx.new_page()
        _perform_login(p, base_url, USERS["regular2"]["username"], USERS["regular2"]["password"])
        ctx.storage_state(path=str(state))
        ctx.close()
    return str(state)


@pytest.fixture(scope="session")
def storage_state_admin(browser: Browser, base_url: str) -> str:
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
    ctx = browser.new_context(storage_state=storage_state_regular1)
    page = ctx.new_page()
    install_time_travel(page)
    yield page
    ctx.close()


@pytest.fixture()
def logged_in_admin(browser: Browser, storage_state_admin: str) -> Generator[Page, None, None]:
    ctx = browser.new_context(storage_state=storage_state_admin)
    page = ctx.new_page()
    install_time_travel(page)
    yield page
    ctx.close()


@pytest.fixture()
def expire_session(page: Page):
    """
    Advance the logical time beyond SESSION_MINUTES to force expiry.
    """
    def _go():
        advance_minutes(page, settings.session_minutes + 1)
    return _go


@pytest.fixture()
def logout(page: Page):
    """
    UI logout via header component, when visible.
    """
    from pages.base_page import BasePage
    b = BasePage(page)
    def _go():
        try:
            b.header().logout()
        except Exception:
            pass
    return _go

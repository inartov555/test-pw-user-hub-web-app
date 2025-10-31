from __future__ import annotations
import os
import pytest
from typing import Generator
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from .utils.config import Settings, settings as settings_fixture
from .utils.logger import _setup_logging  # noqa: F401
from loguru import logger

def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        settings: Settings = metafunc.config._settings if hasattr(metafunc.config, "_settings") else None
        if settings is None:
            # Build once
            settings = next(settings_fixture(metafunc.config))
            metafunc.config._settings = settings
        metafunc.parametrize("browser_name", settings.browsers, scope="session")

@pytest.fixture(scope="session")
def settings(pytestconfig) -> Settings:
    s = next(settings_fixture(pytestconfig))
    pytestconfig._settings = s
    return s

@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(pw, browser_name: str, settings: Settings) -> Generator[Browser, None, None]:
    logger.info(f"Launching browser: {browser_name}")
    browser = getattr(pw, browser_name).launch(headless=not settings.headed)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser, settings: Settings) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(base_url=settings.base_url, record_video_dir="videos" if settings.video else None)
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page
    page.close()

# Auth helpers
@pytest.fixture
def login_as_admin(page: Page, settings: Settings):
    from .pages.login_page import LoginPage
    lp = LoginPage(page)
    lp.open(settings.base_url)
    lp.login(settings.admin_user, settings.admin_pass)
    return page

@pytest.fixture
def login_as_user1(page: Page, settings: Settings):
    from .pages.login_page import LoginPage
    lp = LoginPage(page)
    lp.open(settings.base_url)
    lp.login(settings.user1, settings.user1_pass)
    return page

@pytest.fixture
def login_as_user2(page: Page, settings: Settings):
    from .pages.login_page import LoginPage
    lp = LoginPage(page)
    lp.open(settings.base_url)
    lp.login(settings.user2, settings.user2_pass)
    return page

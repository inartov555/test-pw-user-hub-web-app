
from __future__ import annotations
import logging, os, pytest
from typing import Generator
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, expect
from config.settings import cfg
from config.logging_conf import setup_logging
from utils.api_client import ApiClient

setup_logging()
log = logging.getLogger("qa")

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=cfg.base_url)
    parser.addoption("--api-url", action="store", default=cfg.api_url)
    parser.addoption("--headed", action="store_true")
    parser.addoption("--browsers", action="store", default=os.getenv("BROWSERS","chromium,firefox,webkit"))
    parser.addoption("--locale", action="store", default=cfg.locale)

def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        names = metafunc.config.getoption("--browsers").split(",")
        names = [n.strip() for n in names if n.strip()]
        metafunc.parametrize("browser_name", names, scope="session")

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright, browser_name, pytestconfig) -> Browser:
    headless = not pytestconfig.getoption("--headed")
    return getattr(playwright, browser_name).launch(headless=headless)

@pytest.fixture(scope="session")
def api(pytestconfig) -> ApiClient:
    api = ApiClient(pytestconfig.getoption("--api-url"))
    api.login(cfg.admin.username, cfg.admin.password)
    return api

@pytest.fixture(scope="function")
def context(browser: Browser, pytestconfig) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(locale=pytestconfig.getoption("--locale"), storage_state={"origins": []})
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    p = context.new_page()
    yield p
    p.close()

def ui_login(page: Page, username: str, password: str):
    page.goto(cfg.base_url + "/login")
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()
    expect(page).to_have_url(lambda u: "/users" in u or "/profile" in u)

@pytest.fixture(scope="function")
def login_admin(page: Page):
    ui_login(page, cfg.admin.username, cfg.admin.password)
    yield page
    try:
        page.get_by_role("button", name="Logout").click(timeout=1000)
    except Exception:
        pass

@pytest.fixture(scope="function")
def login_user1(page: Page):
    ui_login(page, cfg.regular1.username, cfg.regular1.password)
    yield page
    try:
        page.get_by_role("button", name="Logout").click(timeout=1000)
    except Exception:
        pass

@pytest.fixture(scope="function")
def set_idle_short(api: ApiClient):
    orig = api.get_settings()
    api.update_settings({"IDLE_TIMEOUT_SECONDS": 3, "ACCESS_TOKEN_LIFETIME": max(60, orig.get("ACCESS_TOKEN_LIFETIME", 1800))})
    yield
    api.update_settings(orig)

@pytest.fixture(scope="function")
def seeded_users(api: ApiClient):
    created = []
    data = [
        ("amy",  "amy@example.com",  "Amy",  "Zeta"),
        ("amy2", "amy2@example.com", "Amy",  "Alpha"),
        ("ben",  "ben@example.com",  "Ben",  "Bravo"),
        ("zoe",  "zoe@example.com",  "Zoe",  "Echo"),
        ("zoe2", "zoe2@example.com", "Zoe",  "Alpha"),
    ]
    for u,e,f,l in data:
        created.append(api.create_user(u,e,f,l))
    yield created
    for u in created:
        try: api.delete_user(u["id"])
        except Exception: pass

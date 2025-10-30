"""Login page tests."""
import pytest
from playwright.sync_api import expect
from .pages.login_page import LoginPage

@pytest.mark.smoke
def test_login_success_user1(page):
    lp = LoginPage(page, page.url.rstrip("/"))
    lp.open()
    lp.login("test1", "megaboss19")
    expect(page.get_by_text("Hi, test1")).to_be_visible()

def test_login_success_admin(page):
    lp = LoginPage(page, page.url.rstrip("/"))
    lp.open()
    lp.login("admin", "changeme123")
    expect(page.get_by_role("link", name="Users")).to_be_visible()

def test_login_invalid_creds(page):
    lp = LoginPage(page, page.url.rstrip("/"))
    lp.open()
    lp.login("no_such_user", "badpass")
    expect(page.get_by_text("Invalid username or password")).to_be_visible()

def test_login_links(page):
    lp = LoginPage(page, page.url.rstrip("/"))
    lp.open()
    page.get_by_role("link", name="Create account").click()
    expect(page).to_have_url(lambda u: "/signup" in u)
    page.go_back()
    page.get_by_role("link", name="Forgot password").click()
    expect(page).to_have_url(lambda u: "/reset-password" in u)

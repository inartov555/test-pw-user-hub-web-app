from playwright.sync_api import expect
from .pages.login_page import LoginPage

def test_login_success_admin(page, settings):
    lp = LoginPage(page)
    lp.open(settings.base_url)
    lp.login(settings.admin_user, settings.admin_pass)
    expect(page).to_have_url(lambda u: "/users" in u)

def test_login_failure(page, settings):
    lp = LoginPage(page)
    lp.open(settings.base_url)
    lp.login("nope", "bad")
    lp.assert_error()


import pytest
from pages.login_page import LoginPage

@pytest.mark.ui
@pytest.mark.smoke
def test_login_success(page):
    lp = LoginPage(page)
    lp.login("test1", "megaboss19")

@pytest.mark.ui
def test_login_failure(page):
    lp = LoginPage(page)
    lp.goto()
    page.get_by_placeholder("Username").fill("unknown")
    page.get_by_placeholder("Password").fill("badpass")
    page.get_by_role("button", name="Sign in").click()
    lp.expect_error()

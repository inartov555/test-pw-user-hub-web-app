"""Login page coverage.

- Valid logins for regular users and admin
- Invalid creds show error
- Session TTL respected (short duration auto-expire)
"""
import os
import pytest
from tests.fixtures.auth_fixtures import login

@pytest.mark.smoke
@pytest.mark.parallel
@pytest.mark.parametrize("username,password", [
    (os.getenv("USER1"), os.getenv("USER1_PASS")),
    (os.getenv("USER2"), os.getenv("USER2_PASS")),
    (os.getenv("ADMIN_USER"), os.getenv("ADMIN_PASS")),
])
def test_login_success(page, login_page, username, password):
    login(page, username, password)

def test_login_invalid_credentials_shows_error(page, login_page):
    login_page.goto()
    login_page.username.fill("nope")
    login_page.password.fill("wrongpass")
    login_page.submit.click()
    assert login_page.error.is_visible()

@pytest.mark.session(minutes=1)
def test_session_expires_according_to_ttl(page, dashboard_page):
    page.wait_for_timeout(62000)
    page.goto("/dashboard")
    assert "/login" in page.url

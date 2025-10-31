"""
End-to-end login flow tests using Playwright and pytest.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from utils.test_data import USERS, VALIDATION


@pytest.mark.smoke
def test_login_success_regular(base_url, page):
    """
    User can log in with valid regular credentials and land on a protected page.
    """
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login(USERS["regular1"]["username"], USERS["regular1"]["password"])
    expect(page).to_have_url(lambda u: "/users" in u or "/dashboard" in u)


def test_login_success_admin(base_url, page):
    """
    Admin can log in successfully and reach an admin-only/protected area.
    """
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login(USERS["admin"]["username"], USERS["admin"]["password"])
    expect(page).to_have_url(lambda u: "/users" in u or "/admin" in u)


@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("", "", "Username"),
        (USERS["regular1"]["username"], "", "Password"),
        ("notexist", "badpass", VALIDATION["invalid_credentials"]),
    ],
)
def test_login_validation_messages(base_url, page, username, password, expected):
    """
    Show validation for empty fields and invalid credentials.

    Args:
        base_url: Base URL of the application under test.
        page: Playwright Page instance.
        username: Username value to submit (may be empty).
        password: Password value to submit (may be empty).
        expected: Expected validation/error text to be visible.
    """
    lp = LoginPage(page, base_url)
    lp.open()
    if username:
        lp.username.fill(username)
    if password:
        lp.password.fill(password)
    lp.login_btn.click()
    expect(page.get_by_text(expected, exact=False)).to_be_visible()


@pytest.mark.regression
def test_login_remember_me_sets_persistent_storage(base_url, page):
    """
    'Remember me' should persist authentication via storage (cookie/localStorage).
    """
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login(USERS["regular2"]["username"], USERS["regular2"]["password"], remember=True)

    state = page.context.storage_state()
    assert any(
        c.get("name", "").lower().find("auth") >= 0 for c in state.get("cookies", [])
    ) or state.get("origins"), "Expected some auth storage to persist."


@pytest.mark.regression
def test_redirects_to_login_when_unauthenticated(base_url, page):
    """
    Direct navigation to a protected route should redirect to /login.
    """
    page.goto(base_url + "/users")
    expect(page).to_have_url(lambda u: "/login" in u)

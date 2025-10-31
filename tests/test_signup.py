"""
End-to-end sign-up flows and validation tests using Playwright + pytest.
"""

from __future__ import annotations
import time

import pytest
from playwright.sync_api import expect

from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from utils.test_data import VALIDATION, USERS


@pytest.mark.regression
def test_signup_happy_path_then_login(base_url, page):
    """
    User can register and then log in with new credentials.
    """
    sp = SignupPage(page, base_url)
    sp.open()
    uid = str(int(time.time()))
    uname = f"qa_{uid}"
    sp.register(uname, f"{uname}@example.com", "StrongPassw0rd!", "StrongPassw0rd!")

    expect(page).to_have_url(lambda u: "/login" in u or "/users" in u or "/dashboard" in u)

    if "/login" in page.url:
        lp = LoginPage(page, base_url)
        lp.login(uname, "StrongPassw0rd!")
        expect(page).to_have_url(lambda u: "/users" in u or "/dashboard" in u)


@pytest.mark.parametrize(
    "username,email,password,confirm,expected",
    [
        ("", "", "", "", "Username"),
        ("newguy", "not-an-email", "StrongPassw0rd!", "StrongPassw0rd!", "email"),
        ("newguy2", "guy2@example.com", "short", "short", VALIDATION["password_strength"]),
        (
            USERS["regular1"]["username"],
            "taken@example.com",
            "StrongPassw0rd!",
            "StrongPassw0rd!",
            VALIDATION["username_taken"],
        ),
        ("mismatch", "mismatch@example.com", "StrongPassw0rd!", "Different1!", "match"),
    ],
)
@pytest.mark.regression
def test_signup_validation(base_url, page, username, email, password, confirm, expected):
    """
    Shows validation errors for empty/invalid fields and mismatched credentials.
    """
    sp = SignupPage(page, base_url)
    sp.open()
    sp.register(username, email, password, confirm)
    expect(page.get_by_text(expected, exact=False)).to_be_visible()

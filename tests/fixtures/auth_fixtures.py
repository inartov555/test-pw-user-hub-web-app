"""Authentication helpers and fixtures.

Implements reliable login/logout flows via POMs. Assumes /login route.
"""
from __future__ import annotations
import os
from tests.pages.login_page import LoginPage

def login(page, username=None, password=None):
    lp = LoginPage(page)
    lp.goto()
    lp.login(username or os.getenv("USER1"), password or os.getenv("USER1_PASS"))

def logout(page):
    from tests.pages.dashboard_page import DashboardPage
    DashboardPage(page).logout()

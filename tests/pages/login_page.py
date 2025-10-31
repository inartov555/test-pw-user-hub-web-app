"""Login page object."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    """Represents /login page with username/password form."""
    path = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username = page.get_by_placeholder("Username").or_(page.get_by_label("Username"))
        self.password = page.get_by_placeholder("Password").or_(page.get_by_label("Password"))
        self.submit = page.get_by_role("button", name="Sign in").or_(page.get_by_role("button", name="Log in"))
        self.error = page.get_by_role("alert").or_(page.locator("[data-test=login-error]"))

    def login(self, user: str, pwd: str):
        self.goto()
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()
        expect(self.page).to_have_url(lambda u: "/dashboard" in u or "/home" in u)

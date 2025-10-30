"""Login page object."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base import BasePage

class LoginPage(BasePage):
    path = "/login"
    def open(self):
        self.goto(self.path)
        expect(self.page.get_by_role("heading", name="Sign in")).to_be_visible()

    def login(self, username: str, password: str):
        self.page.get_by_label("Username").fill(username)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()

    def assert_error(self):
        expect(self.page.get_by_text("Invalid username or password").first).to_be_visible()

    def goto_signup(self):
        self.page.get_by_role("link", name="Create account").click()

    def goto_reset(self):
        self.page.get_by_role("link", name="Forgot password").click()

"""Login page object."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    path = "/login"

    def open(self, base_url: str) -> None:
        self.goto(base_url + self.path)
        expect(self.page.get_by_role("heading", name=lambda n: "Log" in n or "Sign in" in n)).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.page.get_by_placeholder("Username").fill(username)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name=lambda n: "Log in" in n or "Login" in n).click()

    def assert_error(self) -> None:
        expect(self.page.get_by_text("Invalid", exact=False)).to_be_visible()

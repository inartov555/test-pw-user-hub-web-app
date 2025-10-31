
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    path = "/login"
    def login(self, username: str, password: str):
        self.goto()
        self.page.get_by_placeholder("Username").fill(username)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
        expect(self.page).to_have_url(lambda u: "/users" in u or "/profile" in u)
    def expect_error(self):
        expect(self.page.get_by_text("Login failed")).to_be_visible()


from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class SignupPage(BasePage):
    path = "/signup"
    def signup(self, username: str, email: str, password: str):
        self.goto()
        self.page.get_by_placeholder("Email").fill(email)
        self.page.get_by_placeholder("Username").fill(username)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Create account").click()
        expect(self.page.get_by_text("Signup failure").or_(self.page.get_by_text("Hi,"))).to_be_visible()

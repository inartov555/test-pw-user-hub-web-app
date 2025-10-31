from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class SignupPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.path = "/signup"

    @property
    def username(self):
        return self.page.get_by_label("Username", exact=False)

    @property
    def email(self):
        return self.page.get_by_label("Email", exact=False)

    @property
    def password(self):
        return self.page.get_by_label("Password", exact=False)

    @property
    def confirm(self):
        return self.page.get_by_label("Confirm", exact=False)

    @property
    def signup_btn(self):
        return self.page.get_by_role("button", name=lambda n: "sign up" in n.lower() or "register" in n.lower())

    def open(self) -> None:
        self.goto(self.base_url + self.path)

    def register(self, username: str, email: str, password: str, confirm: str | None = None) -> None:
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)
        self.confirm.fill(confirm or password)
        self.signup_btn.click()

    def expect_validation(self, text: str) -> None:
        expect(self.page.get_by_text(text)).to_be_visible()

from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):
    """Interactions and assertions for /login."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.path = "/login"

    @property
    def username(self):
        return self.page.get_by_label("Username", exact=False)

    @property
    def password(self):
        return self.page.get_by_label("Password", exact=False)

    @property
    def login_btn(self):
        return self.page.get_by_role("button", name=lambda n: "log in" in n.lower() or "sign in" in n.lower())

    @property
    def remember_me(self):
        return self.page.get_by_label("Remember", exact=False)

    @property
    def sign_up_link(self):
        return self.page.get_by_role("link", name=lambda n: "sign up" in n.lower() or "register" in n.lower())

    def open(self) -> None:
        self.goto(self.base_url + self.path)

    def login(self, username: str, password: str, remember: bool | None = None) -> None:
        self.username.fill(username)
        self.password.fill(password)
        if remember is True:
            try:
                self.remember_me.check()
            except Exception:
                pass
        self.login_btn.click()

    def expect_validation(self, text: str) -> None:
        expect(self.page.get_by_text(text)).to_be_visible()

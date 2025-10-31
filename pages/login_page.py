"""
Page object for the /login view and its interactions.
"""

from __future__ import annotations

from playwright.sync_api import Page, expect

from .base_page import BasePage


class LoginPage(BasePage):
    """
    Interactions and assertions for the login page.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize the page with a Playwright page and application base URL.
        """
        super().__init__(page)
        self.base_url = base_url
        self.path = "/login"

    @property
    def username(self):
        """
        Locator for the username input.
        """
        return self.page.get_by_label("Username", exact=False)

    @property
    def password(self):
        """
        Locator for the password input.
        """
        return self.page.get_by_label("Password", exact=False)

    @property
    def login_btn(self):
        """
        Locator for the Log in / Sign in button (case-insensitive).
        """
        return self.page.get_by_role(
            "button",
            name=lambda n: "log in" in n.lower() or "sign in" in n.lower(),
        )

    @property
    def remember_me(self):
        """
        Locator for the 'Remember me' checkbox.
        """
        return self.page.get_by_label("Remember", exact=False)

    @property
    def sign_up_link(self):
        """
        Locator for the Sign up / Register link (case-insensitive).
        """
        return self.page.get_by_role(
            "link",
            name=lambda n: "sign up" in n.lower() or "register" in n.lower(),
        )

    def open(self) -> None:
        """
        Navigate directly to the login page.
        """
        self.goto(self.base_url + self.path)

    def login(self, username: str, password: str, remember: bool | None = None) -> None:
        """Fill credentials and submit the form.

        Args:
            username: Username or email to input.
            password: Password to input.
            remember: If True, attempts to check 'Remember me'. If False/None, leaves as-is.
        """
        self.username.fill(username)
        self.password.fill(password)
        if remember is True:
            try:
                self.remember_me.check()
            except TimeoutError:
                # Checkbox may be absent on some variants; ignore.
                pass
        self.login_btn.click()

    def expect_validation(self, text: str) -> None:
        """
        Assert that a validation/error message containing `text` is visible.
        """
        expect(self.page.get_by_text(text)).to_be_visible()

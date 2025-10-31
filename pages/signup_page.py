"""Page object for the /signup view and its interactions."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from .base_page import BasePage


class SignupPage(BasePage):
    """
    Interactions and assertions for the sign-up page.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize with a Playwright page and the application base URL.
        """
        super().__init__(page)
        self.base_url = base_url
        self.path = "/signup"

    @property
    def username(self):
        """
        Locator for the username input.
        """
        return self.page.get_by_label("Username", exact=False)

    @property
    def email(self):
        """
        Locator for the email input.
        """
        return self.page.get_by_label("Email", exact=False)

    @property
    def password(self):
        """
        Locator for the password input.
        """
        return self.page.get_by_label("Password", exact=False)

    @property
    def confirm(self):
        """
        Locator for the password confirmation input.
        """
        return self.page.get_by_label("Confirm", exact=False)

    @property
    def signup_btn(self):
        """
        Locator for the Sign up / Register button (case-insensitive).
        """
        return self.page.get_by_role(
            "button",
            name=lambda n: "sign up" in n.lower() or "register" in n.lower(),
        )

    def open(self) -> None:
        """
        Navigate directly to the sign-up page.
        """
        self.goto(self.base_url + self.path)

    def register(self, username: str, email: str, password: str, confirm: str | None = None) -> None:
        """Fill the registration form and submit.

        Args:
            username: Desired username.
            email: Account email address.
            password: Desired password.
            confirm: Optional confirmation; defaults to `password`.
        """
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)
        self.confirm.fill(confirm or password)
        self.signup_btn.click()

    def expect_validation(self, text: str) -> None:
        """
        Assert that a validation/error message containing `text` is visible.
        """
        expect(self.page.get_by_text(text)).to_be_visible()

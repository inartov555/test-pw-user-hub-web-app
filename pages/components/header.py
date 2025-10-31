"""
Header (top navigation bar) component helpers.
"""

from __future__ import annotations

from playwright.sync_api import Page


class Header:
    """
    Represents the application's top navigation bar.
    """

    def __init__(self, page: Page) -> None:
        """
        Store the Playwright page used by this component.
        """
        self.page = page

    @property
    def logout_button(self):
        """
        Locator for the 'Log out' button (case-insensitive).
        """
        return self.page.get_by_role("button", name=lambda n: "log out" in n.lower())

    def logout(self) -> None:
        """
        Click the 'Log out' button if it is visible; ignore if absent.
        """
        try:
            if self.logout_button.is_visible():
                self.logout_button.click()
        except TimeoutError:
            # Allow tests to proceed if the control isn't present in a given build.
            pass

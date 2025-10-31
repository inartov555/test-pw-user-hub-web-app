from __future__ import annotations
from playwright.sync_api import Page

class Header:
    """Represents the top navigation bar."""
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def logout_button(self):
        return self.page.get_by_role("button", name=lambda n: "log out" in n.lower())

    def logout(self) -> None:
        try:
            if self.logout_button.is_visible():
                self.logout_button.click()
        except Exception:
            pass

"""
Toast (status) component assertions for transient notifications.
"""

from __future__ import annotations

from playwright.sync_api import Page, expect


class Toast:
    """
    Helper for asserting toast/status messages.
    """

    def __init__(self, page: Page) -> None:
        """
        Store the Playwright page used by this component.
        """
        self.page = page

    def expect_message(self, text: str) -> None:
        """
        Assert that a toast/status element contains the given text.
        """
        toast = self.page.get_by_role("status")
        expect(toast).to_contain_text(text)

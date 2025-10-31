"""Settings page object (admin-only)."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class SettingsPage(BasePage):
    path = "/settings"

    def open(self, base_url: str) -> None:
        self.goto(base_url + self.path)
        expect(self.page.get_by_role("heading", name=lambda n: "Settings" in n)).to_be_visible()

    def set_idle_timeout(self, seconds: int) -> None:
        # assumes there's a number input with label containing IDLE or Timeout
        self.page.get_by_label(lambda n: "timeout" in n.lower()).fill(str(seconds))
        self.page.get_by_role("button", name=lambda n: "Save" in n).click()
        expect(self.page.get_by_text("Saved", exact=False)).to_be_visible()

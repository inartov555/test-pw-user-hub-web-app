
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class SettingsPage(BasePage):
    path = "/settings"
    def expect_loaded(self):
        self.goto()
        expect(self.page.get_by_role("heading", name="App Settings")).to_be_visible()
    def set_value(self, label: str, value: str | int):
        self.page.get_by_label(label).fill(str(value))
    def save(self):
        self.page.get_by_role("button", name="Save settings").click()
        expect(self.page.get_by_text("Saved")).to_be_visible()

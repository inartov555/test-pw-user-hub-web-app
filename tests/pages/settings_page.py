"""Settings page object (auth/session settings)."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base import BasePage

class SettingsPage(BasePage):
    path = "/settings"
    def open(self):
        self.goto(self.path)
        expect(self.page.get_by_role("heading", name="App settings")).to_be_visible()

    def set_auth_values(self, renew:int, idle:int, lifetime:int):
        self.page.get_by_label("JWT_RENEW_AT_SECONDS").fill(str(renew))
        self.page.get_by_label("IDLE_TIMEOUT_SECONDS").fill(str(idle))
        self.page.get_by_label("ACCESS_TOKEN_LIFETIME").fill(str(lifetime))

    def save(self):
        self.page.get_by_role("button", name="Save settings").click()
        expect(self.page.get_by_text("The app settings have been saved")).to_be_visible()

    def read_current_values(self) -> tuple[int,int,int]:
        def read_int(label):
            return int(self.page.get_by_label(label).input_value())
        return (
            read_int("JWT_RENEW_AT_SECONDS"),
            read_int("IDLE_TIMEOUT_SECONDS"),
            read_int("ACCESS_TOKEN_LIFETIME"),
        )

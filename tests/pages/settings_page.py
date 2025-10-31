"""Settings page object for theme/locale/session tests."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class SettingsPage(BasePage):
    path = "/settings"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.theme_toggle = page.get_by_role("switch", name="Dark mode").or_(page.locator("[data-test=toggle-theme]"))
        self.locale_select = page.get_by_label("Language").or_(page.locator("[data-test=select-locale] select"))
        self.session_input = page.get_by_label("Session (min)").or_(page.locator("[data-test=session-minutes]"))
        self.save_btn = page.get_by_role("button", name="Save").or_(page.get_by_role("button", name="Update"))

    def set_theme(self, name: str):
        current_dark = self.page.evaluate("() => document.documentElement.getAttribute('data-theme') === 'dark'")
        if name == "dark" and not current_dark:
            self.theme_toggle.click()
        if name == "light" and current_dark:
            self.theme_toggle.click()

    def set_locale(self, code: str):
        self.locale_select.select_option(code)

    def set_session_minutes(self, minutes: int):
        self.session_input.fill(str(minutes))
        self.save_btn.click()

"""Navbar interactions (theme, locale, logout, navigation)."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base import BasePage

class Navbar(BasePage):
    def toggle_additional(self):
        self.page.get_by_role("button", name="Additional").click()

    def nav_to(self, link_text: str):
        self.page.get_by_role("link", name=link_text).click()

    def toggle_dark_mode(self):
        self.page.get_by_role("button", name="Toggle dark mode").click()

    def change_locale_via_storage(self, locale: str):
        # Reliable approach: set i18next language and reload
        self.set_local_storage("i18nextLng", locale)
        self.reload()

    def logout(self):
        # Open user menu then click Sign out
        self.page.get_by_role("button", name="Account").click()
        self.page.get_by_role("menuitem", name="Sign out").click()

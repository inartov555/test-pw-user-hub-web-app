"""Navbar component with language selector and theme toggle."""
from __future__ import annotations
from playwright.sync_api import Page, expect

class Navbar:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def language_select(self):
        return self.page.get_by_role("combobox").filter(has_text="English")  # initial guess; we also allow select[name=''] later

    def select_language(self, locale: str) -> None:
        self.page.locator("select").first.select_option(locale)

    def toggle_additional(self):
        btn = self.page.get_by_role("button", name=lambda n: "Additional" in n or "Add" in n)
        if btn.is_visible():
            btn.click()

    def goto_users(self):
        self.page.get_by_role("link", name=lambda n: "Users" in n).click()

    def goto_settings(self):
        self.toggle_additional()
        self.page.get_by_role("link", name=lambda n: "Settings" in n).click()

    def goto_import_excel(self):
        self.toggle_additional()
        self.page.get_by_role("link", name=lambda n: "Import" in n).click()

    def toggle_theme(self):
        self.page.get_by_role("button", name=lambda n: "dark" in n.lower() or "light" in n.lower()).click()

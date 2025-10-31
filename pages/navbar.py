
from __future__ import annotations
from playwright.sync_api import Page, expect

class Navbar:
    def __init__(self, page: Page):
        self.page = page
    def open_users(self):
        self.page.get_by_role("link", name="Users").click()
    def open_profile(self):
        self.page.get_by_role("link", name="Profile").click()
    def open_settings(self):
        self.page.get_by_role("link", name="App Settings").click()
    def toggle_dark_mode(self):
        self.page.get_by_role("button", name="Toggle dark mode").click()
    def change_locale(self, code: str):
        self.page.locator("nav select").select_option(code)
        expect(self.page.locator("nav select")).to_have_value(code)

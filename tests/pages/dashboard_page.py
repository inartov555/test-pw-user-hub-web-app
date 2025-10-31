"""Dashboard page object."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class DashboardPage(BasePage):
    path = "/dashboard"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.avatar = page.get_by_role("button", name="Account").or_(page.locator("[data-test=avatar]"))
        self.logout_btn = page.get_by_role("menuitem", name="Log out").or_(page.get_by_role("button", name="Log out"))
        self.settings_link = page.get_by_role("link", name="Settings").or_(page.locator("a[href='/settings']"))
        self.users_link = page.get_by_role("link", name="Users").or_(page.locator("a[href='/users']"))

    def logout(self):
        self.avatar.click()
        self.logout_btn.click()
        expect(self.page).to_have_url(lambda u: "/login" in u)

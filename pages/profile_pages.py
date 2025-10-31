
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class ProfileViewPage(BasePage):
    path = "/profile"
    def expect_loaded(self):
        self.goto()
        expect(self.page.get_by_text("Profile")).to_be_visible()

class ProfileEditPage(BasePage):
    path = "/profile-edit"
    def edit_names(self, first: str, last: str):
        self.goto()
        self.page.get_by_label("First name").fill(first)
        self.page.get_by_label("Last name").fill(last)
        self.page.get_by_role("button", name="Save").click()
        expect(self.page.get_by_text("Saved")).to_be_visible()

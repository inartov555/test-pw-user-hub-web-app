"""Profile view/edit page objects."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base import BasePage

class ProfileViewPage(BasePage):
    path = "/profile-view"
    def open(self):
        self.goto(self.path)
        expect(self.page.get_by_role("heading", name="Your profile")).to_be_visible()

class ProfileEditPage(BasePage):
    path = "/profile-edit"
    def open(self):
        self.goto(self.path)
        expect(self.page.get_by_role("heading", name="Edit profile")).to_be_visible()

    def set_first_last(self, first: str, last: str):
        self.page.get_by_label("First name").fill(first)
        self.page.get_by_label("Last name").fill(last)

    def save(self):
        self.page.get_by_role("button", name="Save profile").click()
        expect(self.page.get_by_text("Profile updated")).to_be_visible()

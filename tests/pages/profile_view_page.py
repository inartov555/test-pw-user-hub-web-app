"""Profile View Page.Py POM (placeholder with basic asserts)."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base_page import BasePage

class ProfileView(BasePage):
    path = "/profile"
    def open(self, base_url: str) -> None:
        self.goto(base_url + self.path)
        expect(self.page).to_have_url(lambda u: self.path in u)

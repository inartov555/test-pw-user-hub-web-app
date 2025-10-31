from __future__ import annotations

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all pages."""

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def assert_title_contains(self, text: str) -> None:
        expect(self.page).to_have_title(lambda t: text.lower() in t.lower())

    def assert_url_contains(self, text: str) -> None:
        expect(self.page).to_have_url(lambda u: text in u)

    def toast(self):
        from .components.toast import Toast
        return Toast(self.page)

    def header(self):
        from .components.header import Header
        return Header(self.page)

"""Shared base Page Object utilities for Playwright end-to-end tests."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from .components.toast import Toast
from .components.header import Header


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page):
        """
        Store the Playwright page instance used by this page object.
        """
        self.page = page

    def goto(self, url: str) -> None:
        """
        Navigate the current page to the given URL.
        """
        self.page.goto(url)

    def assert_title_contains(self, text: str) -> None:
        """
        Assert that the page title contains the given text (case-insensitive).
        """
        expect(self.page).to_have_title(lambda t: text.lower() in t.lower())

    def assert_url_contains(self, text: str) -> None:
        """
        Assert that the current URL contains the given substring.
        """
        expect(self.page).to_have_url(lambda u: text in u)

    def toast(self):
        """
        Return the Toast component helper bound to this page.
        """
        return Toast(self.page)

    def header(self):
        """
        Return the Header component helper bound to this page.
        """
        return Header(self.page)

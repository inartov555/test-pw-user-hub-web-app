"""
URL wait helper for Playwright tests.
"""

from __future__ import annotations

from playwright.sync_api import Page, expect


def wait_for_url_includes(page: Page, fragment: str, timeout: int = 5000) -> None:
    """
    Wait until the current URL contains the given fragment.

    Args:
        page: Playwright Page to observe.
        fragment: Substring that should appear in the URL.
        timeout: Max wait time in milliseconds (default: 5000).
    """
    expect(page).to_have_url(lambda url: fragment in url, timeout=timeout)

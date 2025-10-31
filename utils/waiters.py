from __future__ import annotations
from playwright.sync_api import Page, expect

def wait_for_url_includes(page: Page, fragment: str, timeout: int = 5000) -> None:
    expect(page).to_have_url(lambda url: fragment in url, timeout=timeout)

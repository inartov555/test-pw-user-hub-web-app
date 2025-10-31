"""Dashboard page coverage.

- Navigation links visible
- Logout works
- Theme and locale reflected in the DOM
"""
import os
import pytest
from tests.fixtures.auth_fixtures import login

@pytest.mark.smoke
@pytest.mark.parallel
def test_dashboard_navigation_and_logout(page, dashboard_page):
    login(page)
    dashboard_page.goto()
    dashboard_page.users_link.click()
    assert "/users" in page.url
    dashboard_page.logout()

@pytest.mark.theme(name="dark")
@pytest.mark.i18n(name=os.getenv("ALT_LOCALE", "et"))
def test_theme_and_locale_reflected(page, dashboard_page):
    login(page)
    dashboard_page.goto()
    theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
    assert theme == "dark"
    lang = page.evaluate("() => document.documentElement.getAttribute('lang')")
    assert lang == os.getenv("ALT_LOCALE", "et")

"""Settings page tests: theme, locale, session save & reflect across app."""
import os
import pytest
from tests.fixtures.auth_fixtures import login

@pytest.mark.parallel
@pytest.mark.theme(name="dark")
@pytest.mark.i18n(name=os.getenv("ALT_LOCALE", "et"))
def test_change_theme_and_language_persist(page, settings_page, dashboard_page):
    login(page)
    settings_page.goto()
    settings_page.set_theme("dark")
    settings_page.set_locale(os.getenv("ALT_LOCALE", "et"))
    settings_page.set_session_minutes(int(os.getenv("TEST_SESSION_MINUTES", 5)))
    dashboard_page.goto()
    assert page.evaluate("() => document.documentElement.getAttribute('data-theme')") == "dark"
    assert page.evaluate("() => document.documentElement.getAttribute('lang')") == os.getenv("ALT_LOCALE", "et")

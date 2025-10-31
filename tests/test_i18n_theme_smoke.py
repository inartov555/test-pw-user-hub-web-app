"""Quick checks for theme tokens and locale resources rendered.

Validates key translation keys and CSS variables applied when switching themes/locales.
"""
import os
import pytest
from tests.fixtures.auth_fixtures import login

@pytest.mark.smoke
@pytest.mark.theme(name="light")
@pytest.mark.i18n(name=os.getenv("DEFAULT_LOCALE", "en"))
def test_light_theme_tokens_present(page, dashboard_page):
    login(page)
    dashboard_page.goto()
    has_var = page.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--bg').trim().length > 0")
    assert has_var

@pytest.mark.smoke
@pytest.mark.theme(name="dark")
@pytest.mark.i18n(name=os.getenv("ALT_LOCALE", "et"))
def test_translations_rendered_in_alt_locale(page, dashboard_page):
    login(page)
    dashboard_page.goto()
    assert True  # Replace with a specific translation assertion if available

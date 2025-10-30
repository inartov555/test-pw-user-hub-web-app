"""Dark/Light theme and localization checks."""
import pytest
from playwright.sync_api import expect
from .pages.navbar import Navbar

def test_theme_toggle_persists(login_user1):
    page = login_user1
    nb = Navbar(page, page.url.rstrip("/"))
    # Toggle to dark
    nb.toggle_dark_mode()
    # html has class 'dark'
    html = page.locator("html")
    expect(html).to_have_class(lambda c: "dark" in c)
    # reload and ensure still dark
    page.reload()
    expect(html).to_have_class(lambda c: "dark" in c)
    # Toggle back to light
    nb.toggle_dark_mode()
    expect(html).to_have_class(lambda c: "dark" not in c)

@pytest.mark.parametrize("locale,expected_nav", [
    ("en-US", "Users"),
    ("et-EE", "Kasutajad"),
    ("uk-UA", "Користувачі"),
    ("es-ES", "Usuarios"),
])
def test_localization_switch_via_storage(login_user1, locale, expected_nav):
    page = login_user1
    nb = Navbar(page, page.url.rstrip("/"))
    nb.change_locale_via_storage(locale)
    expect(page.get_by_role("link", name=expected_nav)).to_be_visible()

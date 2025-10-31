from playwright.sync_api import expect
from .pages.components.navbar import Navbar

def test_theme_toggle_persists(login_as_user1, settings, page):
    nav = Navbar(page)
    # Check initial theme
    before = page.evaluate("document.documentElement.classList.contains('dark')")
    nav.toggle_theme()
    after = page.evaluate("document.documentElement.classList.contains('dark')")
    assert before != after, "Theme class should toggle"
    # Reload and ensure persisted via localStorage
    page.reload()
    again = page.evaluate("document.documentElement.classList.contains('dark')")
    assert after == again

def test_localization_switch(login_as_user1, settings, page):
    nav = Navbar(page)
    # Switch to Ukrainian, verify a known label changes
    page.locator("select").first.select_option("uk-UA")
    expect(page.get_by_text("Користувачі", exact=False)).to_be_visible()
    # Switch back to English
    page.locator("select").first.select_option("en-US")
    expect(page.get_by_text("Users", exact=False)).to_be_visible()

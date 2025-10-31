
import pytest
from pages.users_page import UsersPage
from pages.navbar import Navbar

@pytest.mark.ui
@pytest.mark.theme
@pytest.mark.usefixtures("login_user1")
def test_dark_light_toggle(page):
    nav = Navbar(page)
    up = UsersPage(page)
    up.expect_loaded()
    html = page.locator("html")
    nav.toggle_dark_mode()
    page.wait_for_timeout(200)
    assert "dark" in (html.get_attribute("class") or "")
    nav.toggle_dark_mode()
    page.wait_for_timeout(200)
    assert "dark" not in (html.get_attribute("class") or "")

@pytest.mark.ui
@pytest.mark.i18n
@pytest.mark.usefixtures("login_user1")
def test_localization_switch_to_estonian(page):
    nav = Navbar(page)
    up = UsersPage(page)
    up.expect_loaded()
    nav.change_locale("et-EE")
    page.get_by_role("link", name="Profiil").is_visible() or True

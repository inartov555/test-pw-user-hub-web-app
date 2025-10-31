
import pytest
from pages.settings_page import SettingsPage

@pytest.mark.ui
@pytest.mark.settings
@pytest.mark.admin
@pytest.mark.usefixtures("login_admin")
def test_change_session_values(page):
    sp = SettingsPage(page)
    sp.expect_loaded()
    sp.set_value("Idle timeout (seconds)", 120)
    sp.set_value("Access token lifetime (seconds)", 600)
    sp.save()

@pytest.mark.ui
@pytest.mark.settings
@pytest.mark.admin
@pytest.mark.usefixtures("login_admin", "set_idle_short")
def test_idle_timeout_logout(page):
    sp = SettingsPage(page)
    sp.expect_loaded()
    page.wait_for_timeout(5000)
    assert "/login" in page.url or page.get_by_role("button", name="Sign in").is_visible()

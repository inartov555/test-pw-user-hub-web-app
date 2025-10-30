"""Settings page tests including temporary override of session settings."""
import pytest
from playwright.sync_api import expect
from .pages.settings_page import SettingsPage
from .pages.navbar import Navbar

@pytest.mark.admin
def test_modify_session_settings(login_admin):
    page = login_admin
    nb = Navbar(page, page.url.rstrip("/"))
    nb.toggle_additional()
    nb.nav_to("Settings")
    sp = SettingsPage(page, page.url.rstrip("/"))
    sp.open()
    orig = sp.read_current_values()
    sp.set_auth_values(renew=300, idle=600, lifetime=900)
    sp.save()
    new_vals = sp.read_current_values()
    assert new_vals == (300,600,900)
    # restore
    sp.set_auth_values(*orig)
    sp.save()

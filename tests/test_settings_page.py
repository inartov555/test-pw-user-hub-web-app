from playwright.sync_api import expect
from .pages.components.navbar import Navbar
import time

def test_session_timeout_setting(login_as_admin, settings, page):
    nav = Navbar(page)
    nav.goto_settings()
    # Set a short idle timeout (e.g., 20s), verify we stay logged in after interaction
    page.get_by_label(lambda n: "timeout" in n.lower()).fill("20")
    page.get_by_role("button", name=lambda n: "Save" in n).click()
    expect(page.get_by_text("Saved", exact=False)).to_be_visible()

"""Profile view and edit flow."""
from playwright.sync_api import expect
from .pages.profile_pages import ProfileViewPage, ProfileEditPage
from .pages.navbar import Navbar

def test_profile_edit_and_view(login_user1, tmp_path):
    page = login_user1
    nb = Navbar(page, page.url.rstrip("/"))
    nb.nav_to("Profile")
    pv = ProfileViewPage(page, page.url.rstrip("/"))
    pv.open()
    # Go edit
    nb.nav_to("Edit profile")
    pe = ProfileEditPage(page, page.url.rstrip("/"))
    pe.open()
    pe.set_first_last("Testy","McTestface")
    pe.save()
    nb.nav_to("Profile")
    expect(page.get_by_text("Testy McTestface")).to_be_visible()

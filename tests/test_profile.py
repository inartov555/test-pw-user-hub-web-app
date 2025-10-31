
import pytest
from pages.profile_pages import ProfileViewPage, ProfileEditPage

@pytest.mark.ui
@pytest.mark.profile
@pytest.mark.usefixtures("login_user1")
def test_profile_edit_and_view(page):
    pe = ProfileEditPage(page)
    pe.edit_names("FirstQA", "LastQA")
    pv = ProfileViewPage(page)
    pv.expect_loaded()

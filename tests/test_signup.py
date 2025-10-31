
import pytest
from pages.signup_page import SignupPage

@pytest.mark.ui
def test_signup_page_renders(page):
    sp = SignupPage(page)
    sp.goto()
    page.get_by_placeholder("Email").is_visible()
    page.get_by_placeholder("Username").is_visible()
    page.get_by_placeholder("Password").is_visible()

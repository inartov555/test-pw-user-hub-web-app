
import pytest

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.usefixtures("login_user1")
def test_stats_page_shows_list(page):
    page.get_by_role("link", name="Stats").click()
    page.locator("ul").first.is_visible()

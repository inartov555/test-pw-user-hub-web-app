from playwright.sync_api import expect
from .pages.users_page import UsersPage
from .pages.components.navbar import Navbar

def test_users_table_visible(login_as_admin, settings, page):
    nav = Navbar(page)
    nav.goto_users()
    up = UsersPage(page)
    up.open(settings.base_url)  # idempotent
    expect(up.visible_rows()).to_be_visible()

def test_global_search_filters(login_as_admin, settings, page):
    nav = Navbar(page)
    nav.goto_users()
    up = UsersPage(page)
    up.searchbox.fill("admin")
    up.searchbox.press("Enter")
    expect(page.locator("table tbody tr")).to_have_count(lambda c: c >= 1)

def test_multi_column_sorting(login_as_admin, settings, page):
    nav = Navbar(page)
    nav.goto_users()
    up = UsersPage(page)
    # Click multiple headers to build multi-sort (the app always multi-sorts)
    up.header("Last name").click()
    up.header("First name").click()
    up.header("Email").click()
    # Expect the sort icons to reflect multi-sort (implicitly, table changes deterministically)
    # Validate the first page rows are sorted by: Email ASC as last click (example)
    emails = [page.locator("table tbody tr >> td:nth-child(3)").nth(i).inner_text().strip() for i in range(min(5, page.locator("table tbody tr").count()))]
    assert emails == sorted(emails), "Email column should be ascending as last header clicked"
    # Clear sort resets
    up.clear_sort()

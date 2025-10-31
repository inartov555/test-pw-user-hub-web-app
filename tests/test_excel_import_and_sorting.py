import tempfile
from pathlib import Path
from playwright.sync_api import expect
from .pages.components.navbar import Navbar
from .pages.excel_import_page import ExcelImportPage
from .pages.users_page import UsersPage
from .utils.excel import make_users_excel

def test_excel_import_and_multi_sort(login_as_admin, settings, page):
    # Prepare Excel test data with deliberate ties to exercise multi-sort + id tiebreaker
    rows = [
        ("zuser1", "alpha@example.com", "Alice", "Zephyr"),
        ("auser2", "alpha@example.com", "Alice", "Zephyr"),  # same email as tiebreaker scenario
        ("buser3", "beta@example.com",  "Bob",   "Yellow"),
        ("cuser4", "beta@example.com",  "Bob",   "Yellow"),
        ("duser5", "beta@example.com",  "Carl",  "Yellow"),
    ]
    with tempfile.TemporaryDirectory() as td:
        xlsx = Path(td) / "import.xlsx"
        make_users_excel(xlsx, rows)
        nav = Navbar(page)
        nav.goto_import_excel()
        imp = ExcelImportPage(page)
        imp.open(settings.base_url)
        imp.upload_file(xlsx)

    # Go to Users and verify multi-column sort (Email ASC then First name DESC, for example)
    nav.goto_users()
    up = UsersPage(page)
    up.header("Email").click()
    up.header("First").click()  # first name
    up.header("First").click()  # desc
    # Expect rows with same Email grouped; within them, First name descending
    # (This is a light check on top N rows; full verification would page through, but we avoid slowness)
    email_cells = [page.locator("table tbody tr >> td:nth-child(3)").nth(i).inner_text().strip() for i in range(min(5, page.locator("table tbody tr").count()))]
    first_cells = [page.locator("table tbody tr >> td:nth-child(1)").nth(i).inner_text().strip() for i in range(min(5, page.locator("table tbody tr").count()))]
    assert email_cells == sorted(email_cells), "Primary Email should be ascending"
    # For entries with same email near the top, ensure first name is descending
    pairs = list(zip(email_cells, first_cells))
    same_email = [p for p in pairs if p[0] == email_cells[0]]
    if len(same_email) >= 2:
        firsts = [p[1] for p in same_email]
        assert firsts == sorted(firsts, reverse=True)

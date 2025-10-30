"""Users table tests including multi-column sorting and pagination."""
import pytest
from playwright.sync_api import expect
from .pages.users_page import UsersPage
from .pages.excel_import_page import ExcelImportPage
from openpyxl import Workbook
from pathlib import Path

def seed_users_excel(tmp_path, page):
    # Create an Excel with deterministic users for sort tests
    wb = Workbook()
    ws = wb.active
    ws.title = "users"
    ws.append(["username","email","first_name","last_name","password","is_staff"])
    rows = [
        ["anna","anna@example.com","Anna","Zephyr","Pwd12345",0],
        ["bob","bob@example.com","Bob","Yellow","Pwd12345",0],
        ["carl","carl@example.com","Carl","Yellow","Pwd12345",1],
        ["dana","dana@example.com","Dana","Alpha","Pwd12345",0],
        ["erik","erik@example.com","Erik","Alpha","Pwd12345",1],
    ]
    for r in rows: ws.append(r)
    f = tmp_path / "seed.xlsx"
    wb.save(f)
    nb = UsersPage(page, page.url.rstrip("/"))
    # Use Excel Import
    from .pages.navbar import Navbar
    nb = Navbar(page, page.url.rstrip("/"))
    nb.toggle_additional()
    nb.nav_to("Import from Excel")
    ip = ExcelImportPage(page, page.url.rstrip("/"))
    ip.open()
    ip.upload_file(str(f))
    return rows

@pytest.mark.admin
def test_users_table_sorting_multi_column(login_admin, tmp_path):
    page = login_admin
    # seed data
    rows = seed_users_excel(tmp_path, page)
    up = UsersPage(page, page.url.rstrip("/"))
    up.open()
    # Sort by last_name asc, then first_name asc to create a stable order
    up.sort_by("Last name", times=1)
    up.sort_by("First name", times=1)
    table = up.get_table_text()
    # Extract visible name columns (assumes order: username, email, first, last, ...)
    names = [(r[2], r[3]) for r in table[:5]]
    # Expected order by last asc then first asc
    expected = sorted([(r[2], r[3]) for r in rows], key=lambda x:(x[1], x[0]))
    assert names[:5] == expected

def test_users_table_pagination(login_admin):
    page = login_admin
    up = UsersPage(page, page.url.rstrip("/"))
    up.open()
    expect(page.get_by_role("combobox", name="Page size")).to_be_visible()
    page.get_byRole = page.get_by_role # alias
    page.get_by_role("combobox", name="Page size").select_option("10")
    expect(page.locator("table tbody tr")).to_have_count(10)

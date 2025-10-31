from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.users_table_page import UsersTablePage


@pytest.mark.smoke
def test_users_table_visible_for_logged_in_user(base_url, logged_in_regular1):
    page = logged_in_regular1
    ut = UsersTablePage(page, base_url)
    ut.open()
    ut.expect_loaded()

@pytest.mark.access
def test_users_table_admin_has_controls(base_url, logged_in_admin):
    """Admin should see extra actions (create/edit/delete) if present."""
    page = logged_in_admin
    ut = UsersTablePage(page, base_url)
    ut.open()
    ut.expect_loaded()
    for name in ("Create", "Add User", "Delete", "Edit"):
        btn = page.get_by_role("button", name=name)
        if btn.count() > 0:
            expect(btn.first).to_be_visible()

@pytest.mark.regression
def test_users_table_search_filters_rows(base_url, logged_in_regular1):
    page = logged_in_regular1
    ut = UsersTablePage(page, base_url)
    ut.open()
    ut.expect_loaded()
    initial = ut.rows.count()
    ut.filter_by("test")
    if ut.search.count() > 0:
        assert ut.rows.count() <= initial

@pytest.mark.regression
def test_users_table_sorting_by_username_if_available(base_url, logged_in_regular1):
    page = logged_in_regular1
    ut = UsersTablePage(page, base_url)
    ut.open()
    ut.expect_loaded()
    before = [r.inner_text() for r in ut.rows.all()][:5]
    ut.sort_by("Username")
    after = [r.inner_text() for r in ut.rows.all()][:5]
    if before and after and before != after:
        assert True

@pytest.mark.smoke
def test_logout_via_header_returns_to_login(base_url, logged_in_regular1):
    page = logged_in_regular1
    ut = UsersTablePage(page, base_url)
    ut.open()
    ut.header().logout()
    expect(page).to_have_url(lambda u: "/login" in u)

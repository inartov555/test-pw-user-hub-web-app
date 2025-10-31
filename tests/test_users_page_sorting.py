"""Users page: multi-column sort tests.

Covers:
- Single column ascending/descending
- Multi-column sort (Last name ASC, First name ASC)
- Multi-column with tie-breaker (Role ASC, Last name DESC)
- Sort stability after filter
- Sort persistence after reload
"""
import pytest
from tests.fixtures.auth_fixtures import login

@pytest.mark.sort
@pytest.mark.parallel
def test_single_column_sort_last_name(page, users_page):
    login(page)
    users_page.goto().assert_loaded()
    users_page.sort_by_columns("Last name")
    last_names = users_page.get_table_cells("Last name")
    assert last_names == sorted(last_names)
    users_page.sort_by_columns("Last name")
    last_names_desc = users_page.get_table_cells("Last name")
    assert last_names_desc == sorted(last_names_desc, reverse=True)

@pytest.mark.sort
@pytest.mark.parallel
def test_multi_column_sort_last_then_first(page, users_page):
    login(page)
    users_page.goto().assert_loaded()
    users_page.sort_by_columns("Last name", "First name")
    pairs = list(zip(users_page.get_table_cells("Last name"), users_page.get_table_cells("First name")))
    assert pairs == sorted(pairs, key=lambda p: (p[0], p[1]))

@pytest.mark.sort
@pytest.mark.parallel
def test_multi_column_sort_role_then_last_desc(page, users_page):
    login(page)
    users_page.goto().assert_loaded()
    users_page.sort_by_columns("Role", "Last name")
    users_page.sort_by_columns("Last name")  # toggle DESC
    pairs = list(zip(users_page.get_table_cells("Role"), users_page.get_table_cells("Last name")))

    def expected(items):
        out = []
        from itertools import groupby
        for role, group in groupby(sorted(items, key=lambda p: (p[0], p[1])), key=lambda p: p[0]):
            g = [g for g in group]
            out.extend(sorted(g, key=lambda p: p[1], reverse=True))
        return out
    assert pairs == expected(pairs)

@pytest.mark.sort
@pytest.mark.parallel
def test_sort_persists_after_filter_and_reload(page, users_page):
    login(page)
    users_page.goto().assert_loaded()
    users_page.sort_by_columns("Last name", "First name")
    page.get_by_placeholder("Search").fill("Alex")
    page.get_by_placeholder("Search").press("Enter")
    pairs = list(zip(users_page.get_table_cells("Last name"), users_page.get_table_cells("First name")))
    assert pairs == sorted(pairs, key=lambda p: (p[0], p[1]))
    page.reload()
    pairs2 = list(zip(users_page.get_table_cells("Last name"), users_page.get_table_cells("First name")))
    assert pairs2 == sorted(pairs2, key=lambda p: (p[0], p[1]))

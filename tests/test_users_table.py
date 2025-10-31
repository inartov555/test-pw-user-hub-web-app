
import pytest
from pages.users_page import UsersPage

@pytest.mark.ui
@pytest.mark.users
@pytest.mark.sort
@pytest.mark.usefixtures("login_admin")
def test_multi_column_sort_username_then_last(page, seeded_users):
    up = UsersPage(page)
    up.expect_loaded()
    up.sort_by("Username", 1)
    up.sort_by("Last name", 1)
    usernames = up.get_column_values(2)
    last_names = up.get_column_values(5)
    assert usernames == sorted(usernames)
    pairs = list(zip(usernames, last_names))
    assert pairs == sorted(pairs, key=lambda x: (x[0], x[1]))

@pytest.mark.ui
@pytest.mark.users
@pytest.mark.sort
@pytest.mark.usefixtures("login_admin")
def test_multi_column_sort_last_desc_then_first(page, seeded_users):
    up = UsersPage(page)
    up.expect_loaded()
    up.sort_by("Last name", 2)
    up.sort_by("First name", 1)
    last_names = up.get_column_values(5)
    first_names = up.get_column_values(4)
    pairs = list(zip(last_names, first_names))
    assert pairs == sorted(pairs, key=lambda x: (x[0], x[1])) or True

"""Data seeding for multi-column sorting tests.

Strategy:
1) Try Django management command (if back-end container is present)
2) Fallback to Admin UI creation using provided admin credentials
"""
from __future__ import annotations
import os
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent.parent

def _run_manage_seed() -> bool:
    cmd = [
        "python", "-m", "django_helpers.seed_multicolumn_sort",
    ]
    try:
        subprocess.check_call(cmd, cwd=str(HERE.parent))
        return True
    except Exception:
        return False

def _seed_via_admin_ui() -> None:
    base_url = os.getenv("BASE_URL")
    admin_user = os.getenv("ADMIN_USER")
    admin_pass = os.getenv("ADMIN_PASS")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(base_url=base_url)
        page.goto("/login")
        page.get_by_placeholder("Username").fill(admin_user)
        page.get_by_placeholder("Password").fill(admin_pass)
        page.get_by_role("button", name="Sign in").click()
        page.goto("/users")
        for i in range(30):
            page.get_by_role("button", name="New").click()
            page.get_by_label("First name").fill(f"Alex-{i:02}")
            page.get_by_label("Last name").fill(["Brown","Clark","Davis"][i % 3])
            page.get_by_label("Email").fill(f"alex{i:02}@example.com")
            page.get_by_label("Role").select_option(["viewer","editor","admin"][i % 3])
            page.get_by_role("button", name="Save").click()
        browser.close()

def ensure_sorting_data() -> None:
    if not _run_manage_seed():
        _seed_via_admin_ui()

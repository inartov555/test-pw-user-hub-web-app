"""Browser matrix utilities and command-line options.

Adds --all-browsers flag to run Chromium, Firefox, WebKit in parallel via pytest-xdist.
"""
from __future__ import annotations
import pytest

BROWSERS = ["chromium", "firefox", "webkit"]

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--all-browsers",
        action="store_true",
        default=False,
        help="Run each test against chromium, firefox, and webkit.",
    )

def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if metafunc.config.getoption("--all-browsers") and "browser_name" in metafunc.fixturenames:
        metafunc.parametrize("browser_name", BROWSERS, scope="session")

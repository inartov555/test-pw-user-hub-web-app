"""Test configuration helpers and typed settings."""
from __future__ import annotations
from pydantic import BaseModel, Field
import pytest

class Settings(BaseModel):
    base_url: str = Field(default="http://localhost:5173")
    login_path: str = Field(default="/login")
    admin_user: str = Field(default="admin")
    admin_pass: str = Field(default="changeme123")
    user1: str = Field(default="test1")
    user1_pass: str = Field(default="megaboss19")
    user2: str = Field(default="test28")
    user2_pass: str = Field(default="megaboss19")
    browsers: list[str] = Field(default_factory=lambda: ["chromium","firefox","webkit"])
    headed: bool = False
    video: bool = False
    trace: bool = False

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--base-url", action="store", default="http://localhost:5173", help="Base URL for the app") 
    parser.addoption("--browser-list", action="store", default="chromium,firefox,webkit", help="Comma-separated list") 
    parser.addoption("--headed", action="store_true", default=False, help="Run headed") 
    parser.addoption("--video", action="store", choices=["on","off"], default="off", help="Record video") 
    parser.addoption("--trace", action="store", choices=["on","off"], default="off", help="Playwright trace") 

@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    return Settings(
        base_url=str(pytestconfig.getoption("--base-url")),
        browsers=[s.strip() for s in str(pytestconfig.getoption("--browser-list")).split(",") if s.strip()],
        headed=bool(pytestconfig.getoption("--headed")),
        video= str(pytestconfig.getoption("--video")) == "on",
        trace= str(pytestconfig.getoption("--trace")) == "on",
    )

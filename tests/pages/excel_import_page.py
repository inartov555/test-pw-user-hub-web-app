"""Excel import page object (admin-only)."""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import Page, expect
from .base_page import BasePage

class ExcelImportPage(BasePage):
    path = "/import-excel"

    def open(self, base_url: str) -> None:
        self.goto(base_url + self.path)
        expect(self.page.get_by_role("heading", name=lambda n: "Import" in n)).to_be_visible()

    def upload_file(self, xlsx: Path) -> None:
        self.page.set_input_files("input[type=file]", str(xlsx))
        self.page.get_by_role("button", name=lambda n: "Upload" in n or "Import" in n).click()
        expect(self.page.get_by_text("Success", exact=False)).to_be_visible()

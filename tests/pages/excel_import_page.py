"""Excel import page object for seeding test users."""
from __future__ import annotations
from playwright.sync_api import Page, expect
from .base import BasePage

class ExcelImportPage(BasePage):
    path = "/import-excel"
    def open(self):
        self.goto(self.path)
        expect(self.page.get_by_role("heading", name="Import from Excel")).to_be_visible()

    def download_template(self):
        with self.page.expect_download() as dl:
            self.page.get_by_role("button", name="Download template").click()
        return dl.value

    def upload_file(self, filepath: str):
        self.page.set_input_files('input[type="file"]', filepath)
        self.page.get_by_role("button", name="Upload").click()
        expect(self.page.get_by_text("imported")).to_be_visible()

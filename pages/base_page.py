
from __future__ import annotations
from playwright.sync_api import Page, expect
from config.settings import cfg

class BasePage:
    path: str = "/"
    def __init__(self, page: Page):
        self.page = page
    def goto(self):
        self.page.goto(cfg.base_url + self.path)
    def set_locale(self, locale: str):
        self.page.locator("nav select").select_option(locale)

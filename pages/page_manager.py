from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class PageManager:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._login = None
        self._inventory = None

    @property
    def login(self) -> LoginPage:
        if self._login is None:
            self._login = LoginPage(self.page)
        return self._login

    @property
    def inventory(self) -> InventoryPage:
        if self._inventory is None:
            self._inventory = InventoryPage(self.page)
        return self._inventory

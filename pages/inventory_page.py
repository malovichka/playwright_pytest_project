from pages.base_page import BasePage
from pages.components.header import HeaderComponent
from playwright.sync_api import expect, Page
import re


class InventoryPage(BasePage):
    INVENTORY_ENDPOINT = "inventory"
    INVENTORY_PAGE_TITLE = "Products"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = HeaderComponent(page)
        self._filter_panel = page.get_by_test_id("product-sort-container")
        self._page_title = page.get_by_test_id("title")

    def should_be_inventory_page(self):
        self.should_be_inventory_url()
        self.should_have_inventory_header()

    def should_be_inventory_url(self):
        expect(self.page).to_have_url(re.compile(self.INVENTORY_ENDPOINT))

    def should_have_inventory_header(self):
        expect(self._page_title).to_have_text(self.INVENTORY_PAGE_TITLE)
        expect(self._filter_panel).to_be_visible()

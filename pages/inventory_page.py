from pages.base_page import BasePage
from pages.components.header import HeaderComponent
from playwright.sync_api import expect, Page
import re


class InventoryPage(BasePage):
    INVENTORY_ENDPOINT = "inventory"
    INVENTORY_PAGE_TITLE = "Products"
    ITEM_NAME_TEST_ID = "inventory-item-name"
    ITEM_PRICE_TEST_ID = "inventory-item-price"
    ITEM_ADD_TO_CART_BUTTON_LOCATOR = ".btn_inventory"
    REMOVE_BUTTON_TEXT = "Remove"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = HeaderComponent(page)
        self._filter_panel = page.get_by_test_id("product-sort-container")
        self._page_title = page.get_by_test_id("title")
        self._inventory_items = page.get_by_test_id("inventory-item")

    def should_be_inventory_page(self):
        expect(self.page).to_have_url(re.compile(self.INVENTORY_ENDPOINT))
        expect(self._page_title).to_have_text(self.INVENTORY_PAGE_TITLE)
        expect(self._filter_panel).to_be_visible()

    def add_item_by_index(self, index: int) -> dict:
        item = self._inventory_items.nth(index)
        name = item.get_by_test_id(self.ITEM_NAME_TEST_ID).text_content()
        price = item.get_by_test_id(self.ITEM_PRICE_TEST_ID).text_content()
        item.locator(self.ITEM_ADD_TO_CART_BUTTON_LOCATOR).click()
        expect(item.locator(self.ITEM_ADD_TO_CART_BUTTON_LOCATOR)).to_have_text(
            self.REMOVE_BUTTON_TEXT
        )
        return {"name": name, "price": price, "quantity": "1"}

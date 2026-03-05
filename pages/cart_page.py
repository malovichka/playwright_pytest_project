from pages.base_page import BasePage
from playwright.sync_api import expect, Page
import re


class CartPage(BasePage):
    CART_ENDPOINT = "cart"
    CART_PAGE_TITLE = "Your Cart"
    CART_ITEM_NAME_TEST_ID = "inventory-item-name"
    CART_ITEM_PRICE_TEST_ID = "inventory-item-price"
    CART_ITEM_QUANTITY_TEST_ID = "item-quantity"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._checkout_button = page.get_by_test_id("checkout")
        self._continue_shopping_button = page.get_by_test_id("continue-shopping")
        self._cart_items = page.get_by_test_id("inventory-item")

    def should_be_cart_page(self):
        expect(self.page).to_have_url(re.compile(self.CART_ENDPOINT))
        expect(self.page.get_by_test_id("title")).to_have_text(self.CART_PAGE_TITLE)
        expect(self._checkout_button).to_be_visible()
        expect(self._continue_shopping_button).to_be_visible()

    def get_all_cart_items_data(self):
        items_data = []
        count = self._cart_items.count()
        for i in range(count):
            item = self._cart_items.nth(i)
            name = item.get_by_test_id(self.CART_ITEM_NAME_TEST_ID).text_content()
            price = item.get_by_test_id(self.CART_ITEM_PRICE_TEST_ID).text_content()
            quantity = item.get_by_test_id(
                self.CART_ITEM_QUANTITY_TEST_ID
            ).text_content()
            items_data.append({"name": name, "price": price, "quantity": quantity})

        return items_data

    def go_to_checkout(self):
        self._checkout_button.click()

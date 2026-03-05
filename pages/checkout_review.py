from pages.base_page import BasePage
from pages import helpers as h
from playwright.sync_api import expect, Page
import re


class CheckoutStepTwo(BasePage):
    CHECKOUT_REVIEW_ENDPOINT = "checkout-step-two"
    CHECKOUT_REVIEW_PAGE_TITLE = "Checkout: Overview"
    CHECKOUT_ITEM_NAME_TEST_ID = "inventory-item-name"
    CHECKOUT_ITEM_PRICE_TEST_ID = "inventory-item-price"
    CHECKOUT_QUANTITY_TEST_ID = "item-quantity"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._cancel_button = page.get_by_test_id("cancel")
        self._finish_checkout_button = page.get_by_test_id("finish")
        self._total_after_taxes = page.get_by_test_id("total-label")
        self._total_before_taxes = page.get_by_test_id("subtotal-label")
        self._tax = page.get_by_test_id("tax-label")
        self._checkout_items = page.get_by_test_id("inventory-item")

    def should_be_checkout_review_page(self):
        expect(self.page).to_have_url(re.compile(self.CHECKOUT_REVIEW_ENDPOINT))
        expect(self.page.get_by_test_id("title")).to_have_text(
            self.CHECKOUT_REVIEW_PAGE_TITLE
        )
        expect(self._total_before_taxes).to_be_visible()
        expect(self._tax).to_be_visible()
        expect(self._total_after_taxes).to_be_visible()
        expect(self._cancel_button).to_be_visible()
        expect(self._finish_checkout_button).to_be_visible()

    def get_all_checkout_items_data(self):
        items_data = []
        count = self._checkout_items.count()
        for i in range(count):
            item = self._checkout_items.nth(i)
            name = item.get_by_test_id(self.CHECKOUT_ITEM_NAME_TEST_ID).text_content()
            price = item.get_by_test_id(self.CHECKOUT_ITEM_PRICE_TEST_ID).text_content()
            quantity = item.get_by_test_id(
                self.CHECKOUT_QUANTITY_TEST_ID
            ).text_content()
            items_data.append({"name": name, "price": price, "quantity": quantity})
        return items_data

    def should_be_correct_total_before_taxes(self, expected_total_before_tax: float):
        total_before_tax_text = self._total_before_taxes.text_content()
        if total_before_tax_text is None:
            raise ValueError(f"Total before tax text not found!")
        total_before_tax = h.get_number_from_price_tag(total_before_tax_text)
        assert (
            total_before_tax == expected_total_before_tax
        ), f"Expected total before tax: {expected_total_before_tax}, actual: {total_before_tax}"

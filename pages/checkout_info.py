from pages.base_page import BasePage
from playwright.sync_api import expect, Page
from pages import helpers as h
import re


class CheckoutStepOne(BasePage):
    CHECKOUT_INFO_ENDPOINT = "checkout-step-one"
    CHECKOUT_INFO_PAGE_TITLE = "Checkout: Your Information"
    CHECKOUT_INFO_ERROR_MESSAGES = {
        "postcode_missing": "Error: Postal Code is required",
        "last_name_missing": "Error: Last Name is required",
        "first_name_missing": "Error: First Name is required",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._first_name_input = page.get_by_test_id("firstName")
        self._last_name_input = page.get_by_test_id("lastName")
        self._postal_code = page.get_by_test_id("postalCode")
        self._cancel_button = page.get_by_test_id("cancel")
        self._continue_button = page.get_by_test_id("continue")
        self._checkout_info_error = page.get_by_test_id("error")

    def should_be_checkout_info_page(self):
        expect(self.page).to_have_url(re.compile(self.CHECKOUT_INFO_ENDPOINT))
        expect(self.page.get_by_test_id("title")).to_have_text(
            self.CHECKOUT_INFO_PAGE_TITLE
        )
        expect(self._first_name_input).to_be_visible()
        expect(self._last_name_input).to_be_visible()
        expect(self._postal_code).to_be_visible()

    def fill_checkout_info(self, first_name: str, last_name: str, postcode: str):
        self._first_name_input.fill(first_name)
        self._last_name_input.fill(last_name)
        self._postal_code.fill(postcode)

    def continue_to_checkout_review(self):
        self._continue_button.click()

    def should_be_checkout_info_error(self, error_message):
        expect(self._checkout_info_error).to_be_visible()
        expect(self._checkout_info_error).to_have_text(error_message)

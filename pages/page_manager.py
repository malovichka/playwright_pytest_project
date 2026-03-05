from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info import CheckoutStepOne
from pages.checkout_review import CheckoutStepTwo


class PageManager:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._login = None
        self._inventory = None
        self._cart = None
        self._first_checkout = None
        self._second_checkout = None

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

    @property
    def cart(self) -> CartPage:
        if self._cart is None:
            self._cart = CartPage(self.page)
        return self._cart

    @property
    def checkout_info(self) -> CheckoutStepOne:
        if self._first_checkout is None:
            self._first_checkout = CheckoutStepOne(self.page)
        return self._first_checkout

    @property
    def checkout_review(self) -> CheckoutStepTwo:
        if self._second_checkout is None:
            self._second_checkout = CheckoutStepTwo(self.page)
        return self._second_checkout

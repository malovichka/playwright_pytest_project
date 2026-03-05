from playwright.sync_api import Page, expect


class HeaderComponent:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._cart_icon = page.get_by_test_id("shopping-cart-link")
        self._cart_badge = page.get_by_test_id("shopping-cart-badge")
        self._burger_menu = page.get_by_role("button", name="Open Menu")
        self._close_burger_menu = page.get_by_role("button", name="Close Menu")
        self._all_items_menu_option = page.get_by_test_id("inventory-sidebar-link")
        self._about_menu_option = page.get_by_test_id("about-sidebar-link")
        self._logout_menu_option = page.get_by_test_id("logout-sidebar-link")
        self._reset_app_state_menu_option = page.get_by_test_id("reset-sidebar-link")

    def logout(self):
        self._burger_menu.click()
        self._logout_menu_option.click()

    def go_to_cart(self):
        self._cart_icon.click()

    def reset_app_state(self):
        self._burger_menu.click()
        self._reset_app_state_menu_option.click()
        expect(self._cart_badge).to_be_hidden()
        self._close_burger_menu.click()

    def should_not_be_visible(self):
        expect(self._burger_menu).to_be_hidden()
        expect(self._cart_icon).to_be_hidden()

    def should_have_cart_count(self, expected_count: int):
        expect(self._cart_badge).to_have_text(str(expected_count))

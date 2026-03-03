from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.components.header import HeaderComponent
from pages import helpers as h


class LoginPage(BasePage):
    STANDARD_USER_KEY = "STANDARD_USER_USERNAME"
    STANDARD_PASSWORD_KEY = "STANDARD_USER_PASSWORD"
    LOGIN_ERROR_MESSAGES = {
        "no_password": "Epic sadface: Password is required",
        "no_username": "Epic sadface: Username is required",
        "wrong_credentials": "Epic sadface: Username and password do not match any user in this service",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = HeaderComponent(page)
        self._username_input = page.get_by_placeholder("Username")
        self._password_input = page.get_by_placeholder("Password")
        self._login_button = page.get_by_test_id("login-button")
        self._login_error = page.get_by_test_id("error")

    def load(self):
        self.navigate(self.MAIN_URL)

    def login_as_standard_user(self):
        username, password = h.get_env_var(self.STANDARD_USER_KEY), h.get_env_var(
            self.STANDARD_PASSWORD_KEY
        )
        self.login(username, password)

    def login(self, username: str = "", password: str = ""):
        self._username_input.fill(username)
        self._password_input.fill(password)
        self._login_button.click()

    def should_be_login_page(self):
        expect(self._username_input).to_be_visible()
        expect(self._password_input).to_be_visible()
        expect(self._login_button).to_be_visible()

    def should_be_login_error_message(self, error_message):
        expect(self._login_error).to_be_visible()
        expect(self._login_error).to_have_text(error_message)

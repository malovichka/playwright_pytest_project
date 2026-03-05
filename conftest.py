from playwright.sync_api import Playwright
from pages.page_manager import PageManager
from pages.login_page import LoginPage
from pages.checkout_info import CheckoutStepOne as c
from _pytest.python import Metafunc
from typing import Generator
from pages import helpers as h
import pytest
import dotenv

dotenv.load_dotenv()


def pytest_generate_tests(metafunc: Metafunc):
    if "login_negative_scenario" in metafunc.fixturenames:
        valid_username = h.get_env_var("STANDARD_USER_USERNAME")
        valid_password = h.get_env_var("STANDARD_USER_PASSWORD")
        scenarios = [
            (valid_username, "", LoginPage.LOGIN_ERROR_MESSAGES["no_password"]),
            ("", valid_password, LoginPage.LOGIN_ERROR_MESSAGES["no_username"]),
            (
                valid_username + "1",
                valid_password,
                LoginPage.LOGIN_ERROR_MESSAGES["wrong_credentials"],
            ),
            (
                valid_username,
                valid_password + "1",
                LoginPage.LOGIN_ERROR_MESSAGES["wrong_credentials"],
            ),
        ]

        ids = [
            "missing_password",
            "missing_username",
            "wrong_username",
            "wrong_password",
        ]
        metafunc.parametrize("login_negative_scenario", scenarios, ids=ids)

    if "checkout_info_negative_scenario" in metafunc.fixturenames:
        checkout_data = h.get_info_for_checkout()
        scenarios = [
            (
                checkout_data["first_name"],
                checkout_data["last_name"],
                "",
                c.CHECKOUT_INFO_ERROR_MESSAGES["postcode_missing"],
            ),
            (
                checkout_data["first_name"],
                "",
                checkout_data["postal_code"],
                c.CHECKOUT_INFO_ERROR_MESSAGES["last_name_missing"],
            ),
            (
                "",
                checkout_data["last_name"],
                checkout_data["postal_code"],
                c.CHECKOUT_INFO_ERROR_MESSAGES["first_name_missing"],
            ),
        ]

        ids = ["missing_postcode", "missing_last_name", "missing_first_name"]
        metafunc.parametrize("checkout_info_negative_scenario", scenarios, ids=ids)


@pytest.fixture(scope="session", autouse=True)
def set_test_id(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args) -> dict:
    return {**browser_context_args, "viewport": None}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args) -> dict:
    return {
        **browser_type_launch_args,
        "headless": False,
        "slow_mo": 500,
        "args": ["--start-maximized"],
    }


@pytest.fixture(scope="function")
def app(page) -> PageManager:
    return PageManager(page)


@pytest.fixture(scope="function")
def user(app: PageManager) -> Generator[PageManager, None, None]:
    app.login.load()
    app.login.login_as_standard_user()
    app.inventory.header.reset_app_state()
    yield app
    app.inventory.header.reset_app_state()
    app.inventory.header.logout()
    app.login.should_be_login_page()

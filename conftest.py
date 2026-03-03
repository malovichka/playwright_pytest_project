from playwright.sync_api import Playwright
from pages.page_manager import PageManager
import pytest
import dotenv

dotenv.load_dotenv()


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

from playwright.sync_api import Page, Response


class BasePage:
    MAIN_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> Response | None:
        return self.page.goto(url)

    def get_url(self) -> str:
        return self.page.url

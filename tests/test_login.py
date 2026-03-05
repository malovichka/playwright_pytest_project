from pages.page_manager import PageManager


def test_login_positive(app: PageManager):
    """
    Test Flow:
        1) Open https://www.saucedemo.com/
        2) Input valid credentials and submit login
        3) Verify that login was successfull -  Inventory Page is opened
        4) Log out
    """
    app.login.load()
    app.login.login_as_standard_user()
    app.inventory.should_be_inventory_page()
    app.inventory.header.logout()
    app.inventory.header.should_not_be_visible()
    app.login.should_be_login_page()


def test_login_negative(app: PageManager, login_negative_scenario: tuple):
    """
    Parametrized test (passing invalid credentials set and expected error message), covers 4 negative scenarios:
        - password is not provided
        - username is not provided
        - wrong password provided
        - wrong username provided

    Flow:
        1) Open https://www.saucedemo.com/
        2) Input invalid credentials and submit login
        3) Verify that login was failed - page URL not changed. Verify that error message text is displayed according to credentials mismatch
    """
    username, password, error_message = login_negative_scenario
    app.login.load()
    app.login.login(username, password)
    app.login.should_be_login_page()
    app.login.should_be_login_error_message(error_message)

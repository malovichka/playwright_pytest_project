from pages.page_manager import PageManager
from pages.checkout_info import CheckoutStepOne as c
from pages import helpers as h
import pytest

checkout_data = h.get_info_for_checkout()
negative_scenarios = [
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


@pytest.mark.parametrize("items_count", range(1, 7))
def test_add_items_and_checkout(user: PageManager, items_count: int):
    """
    Parametrized test (passing quantity of items to be added). Positive scenario for adding 1 or more items in cart and full checkout process

    Flow:

    - Preconditions - user is logged in and Inventory URL is opened
        1) Given number of items is added in cart
        2) Go to cart and check that name and price of items in cart - should be data of items from previous step
        3) Proceed to checkout
        4) Fill in all of the mandatory fields on first phase of checkout and continue
        5) On second checkout phase verify that items at checkout match items that were added on main page
        6) Verify that total was calculated accurately
        7) Finish checkout
    - Teardown - reset application state and logout
    """
    user.inventory.should_be_inventory_page()
    added_items = []

    for i in range(items_count):
        item_data = user.inventory.add_item_by_index(i)
        added_items.append(item_data)
    user.inventory.header.should_have_cart_count(items_count)

    user.inventory.header.go_to_cart()
    user.cart.should_be_cart_page()
    cart_items = user.cart.get_all_cart_items_data()
    expected = sorted(added_items, key=lambda x: x["name"])
    actual_cart = sorted(cart_items, key=lambda x: x["name"])

    assert len(expected) == len(
        actual_cart
    ), f"Expected {len(expected)} items in cart, but found {len(actual_cart)}"
    assert (
        expected == actual_cart
    ), f"\nData Mismatch in Cart! \nExpected: {expected} \nActual: {actual_cart}"

    user.cart.go_to_checkout()
    user.checkout_info.should_be_checkout_info_page()
    user.checkout_info.fill_checkout_info(
        checkout_data["first_name"],
        checkout_data["last_name"],
        checkout_data["postal_code"],
    )
    user.checkout_info.continue_to_checkout_review()

    user.checkout_review.should_be_checkout_review_page()
    checkout_items = user.checkout_review.get_all_checkout_items_data()
    actual_checkout = sorted(checkout_items, key=lambda x: x["name"])

    assert len(expected) == len(
        actual_checkout
    ), f"Expected {len(expected)} items in cart, but found {len(actual_checkout)}"
    assert (
        expected == actual_checkout
    ), f"\nData Mismatch in Checkout! \nExpected: {expected} \nActual: {actual_checkout}"

    expected_total_before_taxes = h.calculate_expected_total(added_items)
    user.checkout_review.should_be_correct_total_before_taxes(
        expected_total_before_taxes
    )


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, error_message",
    negative_scenarios,
    ids=["missing_zip", "missing_last", "missing_first"],
)
def test_checkout_stops_when_missing_data(
    user: PageManager,
    first_name: str,
    last_name: str,
    postal_code: str,
    error_message: str,
):
    """
    Parametrized test (passing fields to fill and expected error message), covers 3 negative scenarios when provided checkout data is insufficient:
        - postcode is not provided
        - last name is not provided
        - first name is not provided

    Flow:

    - Preconditions - user is logged in and Inventory URL is opened
        1) Given number of items is added in cart
        2) Go to cart and check that name and price of items in cart - should be data of items from previous step
        3) Proceed to checkout
        4) Fill in only 2 fields and continue
        5) Verify that first checkout was not successfully completed, verify that error message indicates the reason of failure
    - Teardown: reset application state and logout
    """
    user.inventory.should_be_inventory_page()
    added_items = []

    for i in range(2):
        item_data = user.inventory.add_item_by_index(i)
        added_items.append(item_data)
    user.inventory.header.should_have_cart_count(2)

    user.inventory.header.go_to_cart()
    user.cart.should_be_cart_page()
    cart_items = user.cart.get_all_cart_items_data()
    expected = sorted(added_items, key=lambda x: x["name"])
    actual_cart = sorted(cart_items, key=lambda x: x["name"])

    assert len(expected) == len(
        actual_cart
    ), f"Expected {len(expected)} items in cart, but found {len(actual_cart)}"
    assert (
        expected == actual_cart
    ), f"\nData Mismatch in Cart! \nExpected: {expected} \nActual: {actual_cart}"

    user.cart.go_to_checkout()
    user.checkout_info.should_be_checkout_info_page()
    user.checkout_info.fill_checkout_info(first_name, last_name, postal_code)
    user.checkout_info.continue_to_checkout_review()
    user.checkout_info.should_be_checkout_info_error(error_message)
    user.checkout_info.should_be_checkout_info_page()

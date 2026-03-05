import os
from faker import Faker
import re


def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Required environment variable '{key}' is not set!")
    return value


def get_info_for_checkout() -> dict:
    data = Faker()
    return {
        "first_name": data.first_name(),
        "last_name": data.last_name(),
        "postal_code": data.postcode(),
    }


def calculate_expected_total(items: list[dict]) -> float:
    total = 0
    for item in items:
        price = get_number_from_price_tag(item["price"])
        quantity = int(item["quantity"])
        total += price * quantity
    return total


def get_number_from_price_tag(text: str) -> float:
    match = re.search(r"(\d+\.\d+)", text)
    if match:
        return float(match.group(1))
    raise ValueError(f"Valid price not found in text: {text}")

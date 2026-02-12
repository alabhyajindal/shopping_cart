from pathlib import Path

import pytest

from cart import CartItem, ShoppingCart


HOST_DIR = Path(__file__).resolve().parent


def test_valid_cart_has_no_errors() -> None:
    cart = ShoppingCart(plugin_dir=HOST_DIR)

    cart.add_item(CartItem("p1", "Apples", 2, 100, "grocery"))
    cart.add_item(CartItem("p2", "Bread", 1, 300, "grocery"))

    assert len(cart._items) == 2


def test_restricted_category_reports_error() -> None:
    cart = ShoppingCart(plugin_dir=HOST_DIR)

    cart.add_item(CartItem("p1", "Apples", 2, 100, "grocery"))

    with pytest.raises(ValueError) as exc_info:
        cart.add_item(CartItem("p2", "Wine", 1, 1500, "alcohol"))

    message = str(exc_info.value)
    assert "[restricted_categories]" in message
    assert "restricted category" in message


def test_max_total_and_restricted_category_both_reported() -> None:
    cart = ShoppingCart(plugin_dir=HOST_DIR)

    cart.add_item(CartItem("p1", "Apples", 2, 100, "grocery"))

    with pytest.raises(ValueError) as exc_info:
        cart.add_item(CartItem("p2", "Laptop", 1, 2500, "alcohol"))

    message = str(exc_info.value)
    assert "[max_total]" in message
    assert "[restricted_categories]" in message

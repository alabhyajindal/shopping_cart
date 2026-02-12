from cart import CartItem, ShoppingCart


def main() -> None:
    print("Demo: building a cart that is expected to fail validation.\n")

    cart = ShoppingCart()
    print("Step 1/2: adding a valid grocery item...")
    cart.add_item(CartItem("p1", "Apples", 2, 100, "grocery"))

    try:
        print("Step 2/2: adding an item that should fail max_total and restricted_categories...\n")
        cart.add_item(CartItem("p2", "Red Wine", 1, 2500, "alcohol"))
    except ValueError as error:
        print(error)
    else:
        print("Unexpected result: no validation error was raised.")


if __name__ == "__main__":
    main()

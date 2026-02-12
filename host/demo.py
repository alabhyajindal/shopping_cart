from cart import CartItem, ShoppingCart


def main() -> None:
    cart = ShoppingCart()
    cart.add_item(CartItem("p1", "Apples", 2, 100, "grocery"))

    try:
        cart.add_item(CartItem("p2", "Laptop", 1, 2500, "electronics"))
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()

from cart import CartItem, ShoppingCart


def main() -> None:
    cart = ShoppingCart()
    print("Adding Apples worth 200 to cart...")
    cart.add_item(CartItem("p1", "Apples", 2, 100, "grocery"))

    try:
        print("Adding a Laptop worth 2500 to cart...")
        cart.add_item(CartItem("p2", "Laptop", 1, 2500, "alcohol"))
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()

from dataclasses import dataclass, asdict
from typing import List
import json


@dataclass
class CartItem:
    product_id: str
    name: str
    quantity: int
    price_cents: int
    category: str

    def to_dict(self) -> dict:
        return asdict(self)


class ShoppingCart:
    def __init__(self):
        self._items: List[CartItem] = []

    def add_item(self, item: CartItem) -> None:
        self._items.append(item)

    def remove_item(self, product_id: str) -> None:
        self._items = [
            item for item in self._items if item.product_id != product_id]

    def get_items(self) -> List[CartItem]:
        return self._items.copy()

    def total_cents(self) -> int:
        return sum(item.price_cents * item.quantity for item in self._items)

    def to_json(self) -> str:
        return json.dumps({"items": [item.to_dict() for item in self._items]})

    @classmethod
    def from_items(cls, items: List[CartItem]) -> "ShoppingCart":
        cart = cls()
        for item in items:
            cart.add_item(item)
        return cart

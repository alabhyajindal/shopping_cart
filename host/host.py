import json
from dataclasses import dataclass
from typing import Dict, Protocol
from wasmtime import Store

from max_total import Root as MaxTotalRoot


@dataclass
class PluginResult:
    ok: bool
    error: str

    @classmethod
    def from_json(cls, json_str: str) -> "PluginResult":
        data = json.loads(json_str)
        return cls(ok=data["ok"], error=data.get("error", ""))


class CartPlugin(Protocol):
    """Protocol that all cart plugins must implement"""

    def validate(self, store, cart_json: str) -> str: ...


class PluginHost:
    """Host that manages multiple validation plugins"""

    def __init__(self):
        self.store = Store()
        self.plugins: Dict[str, CartPlugin] = {}
        self._load_plugins()

    def _load_plugins(self):
        # Register max-total plugin
        self.plugins["max_total"] = MaxTotalRoot(self.store)
        # Future: self.plugins["restricted_categories"] = RestrictedCategoriesRoot(self.store)

    def validate(self, plugin_name: str, cart_json: str) -> PluginResult:
        """Run a specific plugin by name"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Unknown plugin: {plugin_name}")

        plugin = self.plugins[plugin_name]
        result_json = plugin.validate(self.store, cart_json)
        return PluginResult.from_json(result_json)

    def validate_all(self, cart_json: str) -> Dict[str, PluginResult]:
        """Run all plugins and return results"""
        return {
            name: self.validate(name, cart_json)
            for name in self.plugins.keys()
        }

    def is_valid(self, cart_json: str) -> bool:
        """Check if cart passes all plugin validations"""
        results = self.validate_all(cart_json)
        return all(r.ok for r in results.values())


def main():
    from cart import ShoppingCart, CartItem

    host = PluginHost()

    # Test 1: Valid cart
    cart = ShoppingCart.from_items([
        CartItem("p1", "Apples", 2, 100, "grocery"),
        CartItem("p2", "Milk", 1, 500, "grocery"),
    ])

    print("=== Valid Cart ===")
    results = host.validate_all(cart.to_json())
    for name, result in results.items():
        print(f"{name}: ok={result.ok}, error='{result.error}'")
    print(f"All valid: {host.is_valid(cart.to_json())}")

    # Test 2: Exceeds max
    expensive = ShoppingCart.from_items([
        CartItem("p3", "Laptop", 1, 2500, "electronics"),
    ])

    print("\n=== Expensive Cart ===")
    result = host.validate("max_total", expensive.to_json())
    print(f"max_total: ok={result.ok}, error='{result.error}'")


if __name__ == "__main__":
    main()

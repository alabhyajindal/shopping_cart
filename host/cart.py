import json
import sys
from dataclasses import asdict, dataclass
from importlib import import_module
from pathlib import Path
from typing import Dict, List, Optional

from wasmtime import Store


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
    def __init__(self, plugin_dir: Optional[Path] = None):
        self._items: List[CartItem] = []
        self._store = Store()
        self._plugins: Dict[str, object] = {}
        self._plugin_dir = plugin_dir or Path(__file__).resolve().parent
        self._load_plugins()

    def _load_plugins(self) -> None:
        plugin_path = str(self._plugin_dir)
        if plugin_path not in sys.path:
            sys.path.insert(0, plugin_path)

        for wasm_file in sorted(self._plugin_dir.glob("*.wasm")):
            plugin_name = wasm_file.stem
            module = import_module(plugin_name)
            root_class = getattr(module, "Root")
            self._plugins[plugin_name] = root_class(self._store)

    def _validate_cart(self) -> Optional[str]:
        cart_json = self.to_json()
        errors: List[str] = []
        for plugin_name, plugin in self._plugins.items():
            raw_result = plugin.validate(self._store, cart_json)
            ok, error = self._parse_plugin_result(raw_result)
            if not ok:
                errors.append(f"[{plugin_name}] {error}")
        if errors:
            return "\n".join(errors)
        return None

    def _parse_plugin_result(self, raw_result: str) -> tuple[bool, str]:
        try:
            parsed = json.loads(raw_result)
        except json.JSONDecodeError as exc:
            return False, f"Plugin returned invalid JSON: {exc.msg}"

        if not isinstance(parsed, dict):
            return False, "Plugin returned invalid result shape: expected object"

        ok = parsed.get("ok")
        error = parsed.get("error")

        if not isinstance(ok, bool):
            return False, "Plugin returned invalid result shape: 'ok' must be a boolean"

        if not isinstance(error, str):
            return False, "Plugin returned invalid result shape: 'error' must be a string"

        if ok:
            return True, ""

        return False, error or "Plugin validation failed"

    def add_item(self, item: CartItem) -> None:
        self._items.append(item)
        error = self._validate_cart()
        if error:
            self._items.pop()
            raise ValueError(error)

    def to_json(self) -> str:
        return json.dumps({"items": [item.to_dict() for item in self._items]})

#[allow(warnings)]
mod bindings;

use bindings::Guest;
use serde::{Deserialize, Serialize};

const MAX_TOTAL_CENTS: i64 = 2000;

#[derive(Debug, Deserialize)]
struct CartItem {
    product_id: String,
    name: String,
    quantity: i32,
    price_cents: i64,
    category: String,
}

#[derive(Debug, Deserialize)]
struct ShoppingCart {
    items: Vec<CartItem>,
}

#[derive(Debug, Serialize)]
struct PluginResult {
    ok: bool,
    error: String,
}

struct MaxTotal;

impl MaxTotal {
    fn calculate_total(cart: &ShoppingCart) -> i64 {
        cart.items
            .iter()
            .map(|item| item.price_cents * item.quantity as i64)
            .sum()
    }
}

impl Guest for MaxTotal {
    fn validate(cart_json: String) -> String {
        let cart: ShoppingCart = match serde_json::from_str(&cart_json) {
            Ok(c) => c,
            Err(e) => {
                return serde_json::to_string(&PluginResult {
                    ok: false,
                    error: format!("Invalid JSON: {}", e),
                })
                .unwrap();
            }
        };

        let total = Self::calculate_total(&cart);

        let result = if total > MAX_TOTAL_CENTS {
            PluginResult {
                ok: false,
                error: format!(
                    "Cart total {} cents exceeds maximum {} cents",
                    total, MAX_TOTAL_CENTS
                ),
            }
        } else {
            PluginResult {
                ok: true,
                error: String::new(),
            }
        };

        serde_json::to_string(&result).unwrap()
    }
}

bindings::export!(MaxTotal with_types_in bindings);

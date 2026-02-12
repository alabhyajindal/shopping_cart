#[allow(warnings)]
mod bindings;

use bindings::Guest;
use shared::{parse_cart, CartItem, PluginResult};

const MAX_TOTAL_CENTS: i64 = 2000;

struct MaxTotal;

impl MaxTotal {
    fn calculate_total(items: &[CartItem]) -> i64 {
        items
            .iter()
            .map(|item| item.price_cents * item.quantity as i64)
            .sum()
    }
}

impl Guest for MaxTotal {
    fn validate(cart_json: String) -> String {
        let cart = match parse_cart(&cart_json) {
            Ok(c) => c,
            Err(error) => {
                return PluginResult::error(error).to_json();
            }
        };

        let total = Self::calculate_total(&cart.items);

        let result = if total > MAX_TOTAL_CENTS {
            PluginResult::error(format!(
                "Cart total {} cents exceeds maximum {} cents",
                total, MAX_TOTAL_CENTS
            ))
        } else {
            PluginResult::ok()
        };

        result.to_json()
    }
}

bindings::export!(MaxTotal with_types_in bindings);

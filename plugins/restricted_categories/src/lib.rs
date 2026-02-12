#[allow(warnings)]
mod bindings;

use bindings::Guest;
use shared::{parse_cart, PluginResult};

const RESTRICTED_CATEGORIES: [&str; 2] = ["alcohol", "tobacco"];

struct RestrictedCategories;

impl RestrictedCategories {
    fn is_restricted_category(category: &str) -> bool {
        let normalized = category.trim().to_ascii_lowercase();
        RESTRICTED_CATEGORIES
            .iter()
            .any(|restricted| *restricted == normalized)
    }
}

impl Guest for RestrictedCategories {
    fn validate(cart_json: String) -> String {
        let cart = match parse_cart(&cart_json) {
            Ok(c) => c,
            Err(error) => {
                return PluginResult::error(error).to_json();
            }
        };

        let result = if let Some(item) = cart
            .items
            .iter()
            .find(|item| Self::is_restricted_category(&item.category))
        {
            PluginResult::error(format!(
                "Item '{}' has restricted category '{}'",
                item.name, item.category
            ))
        } else {
            PluginResult::ok()
        };

        result.to_json()
    }
}

bindings::export!(RestrictedCategories with_types_in bindings);

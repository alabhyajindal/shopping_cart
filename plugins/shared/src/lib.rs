use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct CartItem {
    pub product_id: String,
    pub name: String,
    pub quantity: i32,
    pub price_cents: i64,
    pub category: String,
}

#[derive(Debug, Deserialize)]
pub struct ShoppingCart {
    pub items: Vec<CartItem>,
}

#[derive(Debug, Serialize)]
pub struct PluginResult {
    pub ok: bool,
    pub error: String,
}

impl PluginResult {
    pub fn ok() -> Self {
        Self {
            ok: true,
            error: String::new(),
        }
    }

    pub fn error(message: impl Into<String>) -> Self {
        Self {
            ok: false,
            error: message.into(),
        }
    }

    pub fn to_json(&self) -> String {
        serde_json::to_string(self).unwrap()
    }
}

pub fn parse_cart(cart_json: &str) -> Result<ShoppingCart, String> {
    serde_json::from_str(cart_json).map_err(|error| format!("Invalid JSON: {}", error))
}

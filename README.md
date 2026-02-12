# Shopping cart plugin system

Shopping cart implemented in Python with a WebAssembly plugin system. Plugins determine what constitutes a valid cart state. If adding an item to a cart results in an invalid state, then the recently added item is removed, and an error is surfaced to the host.

## Prerequisites

- Python
- Rust
- [Cargo Component](https://github.com/bytecodealliance/cargo-component)
- [Justfile](https://github.com/bytecodealliance/cargo-component)

## Setup

```
git clone git@github.com:alabhyajindal/shopping_cart.git
cd shopping_cart
just build
```

## Usage

Run `python host/demo.py` to view how the validation works in practice. Run `just test` to run the test suite. All tests should pass. [TODO]

TODO: design doc - talk about wasm component model, and add another plugin

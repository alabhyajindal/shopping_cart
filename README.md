# Shopping Cart Plugin System

This project implements a shopping cart in Python with a WebAssembly plugin system. Plugins determine what constitutes a valid cart state. If adding an item makes the cart invalid, the most recently added item is removed and an error is surfaced to the host.

## Prerequisites

- Python
- Rust
- [Cargo Component](https://github.com/bytecodealliance/cargo-component)
- [just](https://github.com/casey/just)

## Setup

```
git clone git@github.com:alabhyajindal/shopping_cart.git
cd shopping_cart
just build
```

## Usage

Run `python host/demo.py` to see validation behavior in practice.
Run `just test` to run the test suite. All tests should pass.

## References

- [An introduction to the WebAssembly component model, Mikkel Mørk Hegnhøj](https://www.youtube.com/watch?v=_fKPvnhX-vI)
- [Extensibility using the WebAssembly Component Model](https://github.com/ThorstenHans/wasmio-2024-demos/tree/main/extensibility)
- [Building a simple component in Rust](https://component-model.bytecodealliance.org/language-support/building-a-simple-component/rust.html)
- [Running components from Python Applications](https://component-model.bytecodealliance.org/language-support/building-a-simple-component/python.html#running-components-from-python-applications)

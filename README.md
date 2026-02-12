# Shopping cart plugin system

Shopping cart implemented in Python with a WebAssembly plugin system. Plugins determine what constitutes a valid cart state. If adding an item to a cart results in an invalid state, then the recently added item is removed, and an error is surfaced to the host.

## Prerequisites

- Python
- Rust
- [Cargo Component](https://github.com/bytecodealliance/cargo-component)
- [Justfile](https://github.com/bytecodealliance/cargo-component)

## Usage

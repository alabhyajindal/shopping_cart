# Design

This project uses the [WebAssembly Component Model](https://component-model.bytecodealliance.org/) to build a shopping cart with a Wasm plugin system.

The interface between Python and Rust is specified using [WIT](https://component-model.bytecodealliance.org/design/wit.html). Data is currently passed as stringified JSON. Ideally, we would model the data directly in WIT, but `wasmtime.bindgen` on the Python side does not fully support the WIT types we need. To counter this limitation while keeping the boundary robust, we use string payloads and enforce validation at both boundaries. Rust validates incoming cart JSON shape on plugin entry. Python validates plugin response JSON shape and verifies that `ok` is a boolean and `error` is a string before using it. We use `cargo component` because the native Rust toolchain targets `wasm32-wasip2`, which pulls in WASI support that `wasmtime.bindgen` does not support in this setup.

Before settling on this solution, we considered creating our own ABI and manually reading from and writing to Wasm linear memory to communicate between host and guest. However, this approach is quite verbose and increases the surface area for errors.

Rust was chosen because of its strong Wasm support. Wasmtime was chosen as the Wasm engine because it is established and has a maintained Python library. JSON, which is stringified before passing, was chosen as the data exchange format because it has strong serialization and deserialization support in both languages.

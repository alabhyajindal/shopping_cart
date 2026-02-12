default: 
    @just --list

max_total: 
    cd plugins/max_total && \
    cargo component build --target wasm32-unknown-unknown --release && \
    cp target/wasm32-unknown-unknown/release/max_total.wasm ../../host/ && \
    cd ../../host && \
    python -m wasmtime.bindgen max_total.wasm --out-dir=max_total

build: 
    just max_total

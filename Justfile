default: 
    @just --list

max_total: 
    cd plugins/max_total && \
    cargo component build --target wasm32-unknown-unknown --release && \
    cp target/wasm32-unknown-unknown/release/max_total.wasm ../../host/ && \
    cd ../../host && \
    python -m wasmtime.bindgen max_total.wasm --out-dir=max_total

restricted_categories:
    cd plugins/restricted_categories && \
    cargo component build --target wasm32-unknown-unknown --release && \
    cp target/wasm32-unknown-unknown/release/restricted_categories.wasm ../../host/ && \
    cd ../../host && \
    python -m wasmtime.bindgen restricted_categories.wasm --out-dir=restricted_categories

build: max_total restricted_categories

test: build
    python -m pytest host/test_cart.py -q

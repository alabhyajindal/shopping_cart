from .intrinsics import _decode_utf8, _encode_utf8, _load
import ctypes
import importlib_resources
import pathlib
import wasmtime

class Root:
    
    def __init__(self, store: wasmtime.Store) -> None:
        file = importlib_resources.files() / ('root.core0.wasm')
        if isinstance(file, pathlib.Path):
            module = wasmtime.Module.from_file(store.engine, file)
        else:
            module = wasmtime.Module(store.engine, file.read_bytes())
        instance0 = wasmtime.Instance(store, module, []).exports(store)
        core_memory0 = instance0["memory"]
        assert(isinstance(core_memory0, wasmtime.Memory))
        self._core_memory0 = core_memory0
        realloc0 = instance0["cabi_realloc"]
        assert(isinstance(realloc0, wasmtime.Func))
        self._realloc0 = realloc0
        post_return0 = instance0["cabi_post_validate"]
        assert(isinstance(post_return0, wasmtime.Func))
        self._post_return0 = post_return0
        lift_callee0 = instance0["validate"]
        assert(isinstance(lift_callee0, wasmtime.Func))
        self.lift_callee0 = lift_callee0
    def validate(self, caller: wasmtime.Store, cart_json: str) -> str:
        ptr, len0 = _encode_utf8(cart_json, self._realloc0, self._core_memory0, caller)
        ret = self.lift_callee0(caller, ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_int32, self._core_memory0, caller, ret, 0)
        load1 = _load(ctypes.c_int32, self._core_memory0, caller, ret, 4)
        ptr2 = load
        len3 = load1
        list = _decode_utf8(self._core_memory0, caller, ptr2, len3)
        tmp = list
        self._post_return0(caller, ret)
        return tmp

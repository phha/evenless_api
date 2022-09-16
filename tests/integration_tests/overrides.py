from collections import UserDict
from collections.abc import Callable
from functools import wraps
from typing import Any, Dict, ParamSpec, Type, TypeVar
from unittest.mock import Mock, create_autospec

from .typing import OverridesKey

_T = TypeVar("_T")
_P = ParamSpec("_P")


class Overrides(UserDict, Dict[Callable[..., Any], Callable[..., Any]]):
    def set_value(self, key: OverridesKey[_P, _T], value: _T) -> _T:
        def mock_fn(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            return value

        self.data[key] = wraps(key)(mock_fn)
        return self.data[key]()

    def mock(self, key: OverridesKey[_P, _T], spec: Type[_T], *args, **kwargs) -> Mock:
        kwargs.setdefault("spec_set", True)
        kwargs.setdefault("instance", True)
        kwargs.setdefault("name", f"mock value for {key}")
        kwargs.setdefault("unsafe", False)
        mock = create_autospec(spec, *args, **kwargs)
        return self.set_value(key, mock)

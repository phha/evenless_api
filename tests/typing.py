from typing import Callable, ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")

OverridesKey = Callable[_P, _T]

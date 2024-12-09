from typing import Any, Callable, Final, List, Optional, Type

import numpy as np
from mypy.plugin import ClassDefContext, Plugin
from mypy.types import Instance

__all__: List[str] = []


def _get_type_fullname(typ: Any) -> str:
    return f"{typ.__module__}.{typ.__qualname__}"


NUMPY_SIGNED_INTEGER_TYPE_FULLNAME: Final = _get_type_fullname(np.signedinteger)
NUMPY_FLOATING_TYPE_FULLNAME: Final = _get_type_fullname(np.floating)
NUMPY_BOOL_TYPE_FULLNAME: Final = _get_type_fullname(np.bool_)


def _promote_bool_callback(ctx: ClassDefContext) -> None:
    """Add two-way type promotion between `bool` and `numpy.bool_`.

    This promotion allows for use of NumPy typing annotations with `bool`,
    e.g. npt.NDArray[bool].

    See mypy.semanal_classprop.add_type_promotion for a similar promotion
    between `int` and `i64` types.
    """
    assert ctx.cls.fullname == NUMPY_BOOL_TYPE_FULLNAME
    numpy_bool: Instance = ctx.api.named_type(NUMPY_BOOL_TYPE_FULLNAME)
    builtin_bool: Instance = ctx.api.named_type("builtins.bool")

    builtin_bool.type._promote.append(numpy_bool)
    numpy_bool.type.alt_promote = builtin_bool


def _promote_int_callback(ctx: ClassDefContext) -> None:
    """Add two-way type promotion between `int` and `numpy.signedinteger`.

    This promotion allows for use of NumPy typing annotations with `int`,
    e.g. npt.NDArray[int].

    See mypy.semanal_classprop.add_type_promotion for a similar promotion
    between `int` and `i64` types.
    """
    assert ctx.cls.fullname == NUMPY_SIGNED_INTEGER_TYPE_FULLNAME
    numpy_signed_integer: Instance = ctx.api.named_type(
        NUMPY_SIGNED_INTEGER_TYPE_FULLNAME
    )
    builtin_int: Instance = ctx.api.named_type("builtins.int")

    builtin_int.type._promote.append(numpy_signed_integer)
    numpy_signed_integer.type.alt_promote = builtin_int


def _promote_float_callback(ctx: ClassDefContext) -> None:
    """Add two-way type promotion between `float` and `numpy.floating`.

    This promotion allows for use of NumPy typing annotations with `float`,
    e.g. npt.NDArray[float].

    See mypy.semanal_classprop.add_type_promotion for a similar promotion
    between `int` and `i64` types.
    """
    assert ctx.cls.fullname == NUMPY_FLOATING_TYPE_FULLNAME
    numpy_floating: Instance = ctx.api.named_type(NUMPY_FLOATING_TYPE_FULLNAME)
    builtin_float: Instance = ctx.api.named_type("builtins.float")

    builtin_float.type._promote.append(numpy_floating)
    numpy_floating.type.alt_promote = builtin_float


class _NptPromotePlugin(Plugin):
    """Mypy plugin to enable type annotations of NumPy arrays with builtin types."""

    def get_customize_class_mro_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        """Customize class definitions before semantic analysis."""
        if fullname == NUMPY_FLOATING_TYPE_FULLNAME:
            return _promote_float_callback
        elif fullname == NUMPY_SIGNED_INTEGER_TYPE_FULLNAME:
            return _promote_int_callback
        elif fullname == NUMPY_BOOL_TYPE_FULLNAME:
            return _promote_bool_callback
        return None


def plugin(version: str) -> Type[_NptPromotePlugin]:
    """Entry-point for mypy."""
    return _NptPromotePlugin

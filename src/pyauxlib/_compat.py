"""Compatibility shims for optional dependencies."""

import functools
from collections.abc import Callable
from typing import Any

try:
    import wrapt
except ImportError:

    class _Wrapt:
        """Minimal fallback for `wrapt` when the `decorators` extra is not installed.

        Only `wrapt.decorator` is replicated. The `instance` argument is always `None`
        (bound-method introspection requires the real `wrapt` package).
        """

        @staticmethod
        def decorator(
            wrapper: Callable[[Callable[..., Any], Any, tuple[Any, ...], dict[str, Any]], Any],
        ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
            """Replicate `wrapt.decorator` using :func:`functools.wraps`."""

            def outer(wrapped: Callable[..., Any]) -> Callable[..., Any]:
                @functools.wraps(wrapped)
                def inner(*args: Any, **kwargs: Any) -> Any:
                    return wrapper(wrapped, None, args, kwargs)

                inner.__wrapped__ = wrapped
                return inner

            return outer

    wrapt = _Wrapt()  # type: ignore[assignment]

__all__ = ["wrapt"]

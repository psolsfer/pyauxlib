"""Utilities for working with callable objects."""
import inspect
import logging
from collections.abc import Callable

from pyauxlib.decorators.warnings import experimental

logger = logging.getLogger(__name__)


@experimental
def call_with_arguments(*args: dict, callable_obj: Callable) -> Callable:
    """Execute a callable object with provided arguments.

    This function checks if the required arguments of a callable object are included in the
    passed arguments, and returns the callable_object(arguments).

    Parameters
    ----------
    *args : dict
        Variable number of dictionaries with arguments to be passed to the callable.
        In case of duplicate entries, the last values from last dictionaries overwrite
        those of the first ones.
    callable_obj : Callable
        Callable object (function, class).

    Returns
    -------
    Callable
        The callable object with the passed arguments.

    Raises
    ------
    TypeError
        If a required argument for the callable object is absent in arguments, if the
        provided object is not callable, or if the provided callable object does not
        accept either *args or **kwargs.
    """
    if callable(callable_obj):
        sig = inspect.signature(callable_obj)
        params = sig.parameters
        callable_accepts_kwargs = sig.varkw is not None
        callable_accepts_args = sig.varargs is not None
    else:
        error_msg = "The provided object is not callable."
        logger.error(error_msg)
        raise TypeError(error_msg)

    if not callable_accepts_args and not callable_accepts_kwargs:
        error_msg = "The provided callable object does not accept *args or **kwargs."
        logger.error(error_msg)
        raise TypeError(error_msg)

    argskwargs = _get_argskwargs(callable_obj)

    # Merge all the dictionaries in *args
    # Values from last dictionaries overwrite existing keys in the previous
    arguments = {key: val for d in args for key, val in d.items()}

    extra_args = {k: v for (k, v) in arguments.items() if k not in params}
    kwargs = {}

    if extra_args:
        if callable_accepts_kwargs:  # Replace with actual check
            kwargs.update(extra_args)
        else:
            logger.warning("Extra arguments were passed: %s", extra_args.keys())
            # Or: raise TypeError(f"Extra arguments were passed: {extra_args}")

    for arg_name, v in params.items():
        # Required argument (doesn't have a default value in callable_object)
        # *args and **kwargs are not required
        required_argument = (
            (v.default == inspect.Parameter.empty) if arg_name not in argskwargs else False
        )

        if required_argument:
            if arg_name in arguments:
                kwargs[arg_name] = arguments[arg_name]
            else:
                error_msg = f"Argument '{arg_name}' is missing"
                raise TypeError(error_msg)
        elif arg_name in arguments:
            kwargs[arg_name] = arguments[arg_name] if arg_name in arguments else v.default

    if callable_accepts_kwargs:
        return callable_obj(**kwargs)

    # Converts the kwargs to args
    args = [kwargs[name] for name in sig.parameters]
    return callable_obj(*args)


def _get_argskwargs(callable_obj: Callable) -> list[str | None]:
    """Return a list with the args and kwargs of a callable.

    Parameters
    ----------
    callable : Callable
        object to check for args and kwargs

    Returns
    -------
    list[str]
        list of args and kwargs
    """
    params_spec = inspect.getfullargspec(callable_obj)

    return [params_spec.varargs, params_spec.varkw]

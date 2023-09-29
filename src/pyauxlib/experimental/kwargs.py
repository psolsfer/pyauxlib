"""Experimental function to check for unknown kwargs."""
from pyauxlib.decorators.warnings import experimental


@experimental
def unknown_kwargs(kwargs: dict, recognized_kwargs: list[str]):
    """Check for unkown kwargs passed to a method/class.

    Parameters
    ----------
    kwargs : dict
        kwargs passed to the caller
    recognized_kwargs : list[str]
        list of kwargs recognized by the caller

    Raises
    ------
    ValueError
        raises a ValueError if unknown arguments are found
    """
    # REFERENCE: based on an implementation found in https://github.com/astropy/specutils

    unknown_kwargs = set(kwargs).difference(recognized_kwargs)

    if unknown_kwargs:
        msg = "Unknown arguments(s): {}.".format(", ".join(map(str, unknown_kwargs)))
        raise ValueError(msg)

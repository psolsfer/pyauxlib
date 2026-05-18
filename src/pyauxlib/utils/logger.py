"""Logging functions."""

import logging
import logging.handlers
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from pyauxlib.fileutils.filesfolders import create_folder

if sys.version_info >= (3, 11):
    from datetime import UTC

    _LOG_LEVELS = logging.getLevelNamesMapping()
else:
    # For Python 3.10
    from datetime import timezone

    UTC = timezone.utc

    _LOG_LEVELS: dict[str, int] = {
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.FATAL,
        "ERROR": logging.ERROR,
        "WARN": logging.WARN,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET,
    }


__all__ = ["ColorFormatter", "init_logger", "setup_null_handler"]


class ColorFormatter(logging.Formatter):
    """Logging formatter adding console colors to the output."""

    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[0;36m",  # Cyan
        "INFO": "\033[0;32m",  # Green
        "WARNING": "\033[0;33m",  # Yellow
        "ERROR": "\033[0;31m",  # Red
        "CRITICAL": "\033[0;35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record as text.

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.

        Returns
        -------
        str
            The formatted log record with color codes.
        """
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"


def _set_level(level: int | str | None, default_level: int | str = "INFO") -> int:
    """Return a correct logging level value.

    Parameters
    ----------
    level : int | str | None
        level of the logger, by "INFO"
        Any of the levels of logging can be passed as a string:
        ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
        Note that lower case letters can also be used
    default_level : int | str, optional
        default level in case that `level` is incorrect, by default "INFO"

    Returns
    -------
    int
        The numeric value of the logging level.

    Raises
    ------
    ValueError
        If the level string is not a valid logging level.
    TypeError
        If the level is not None, int, or str.
    """
    if level is None:
        level = default_level

    if isinstance(level, int):
        return level

    try:
        return _LOG_LEVELS[level.upper()]
    except KeyError as err:
        valid_levels = ", ".join(_LOG_LEVELS)
        error_msg = f"Invalid logging level: {level!r}. Valid levels are: {valid_levels}"
        raise ValueError(error_msg) from err


def init_logger(  # noqa: PLR0913
    name: str = "",
    level: int | str = "INFO",
    level_console: int | str | None = None,
    level_file: int | str | None = None,
    output_folder: Path | None = None,
    file_size: int = 1024 * 1024,
    backup_count: int = 5,
    propagate: bool = True,
    output_console: bool = True,
    colored_console: bool = True,
    output_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """Initialize the logger with enhanced features.

    .. warning::
        This function is intended for **application-level** use only. Do not call it inside a
        reusable library or sub-package — doing so will either swallow logs (``propagate=False``)
        or produce duplicate output (``propagate=True``) from the consuming application's
        perspective. Use :func:`setup_null_handler` in libraries instead.

    Parameters
    ----------
    name : str, optional
        Name of the logger. Use "" (default) to configure the root logger.
        When using non-root loggers, ensure that loggers in other modules fall under the same
        hierarchy (e.g., use ``getLogger("yourapp.module")``).
        If using a named logger, you may need to set ``propagate=True`` and ensure child loggers use
        matching names to inherit handlers and formatting.
    level : int or str, optional
        Overall logging level, by default "INFO".
        Any of the levels of logging can be passed as a string:
        ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'].
        Note that lower case letters can also be used.
    level_console : int or str or None, optional
        Console logging level, by default None (inherits ``level``).
    level_file : int or str or None, optional
        File logging level, by default None (inherits ``level``).
    output_folder : Path or None, optional
        Folder to save log files, by default None (no file output).
    file_size : int, optional
        Maximum size of log files before rotation, by default 1 MB.
    backup_count : int, optional
        Number of rotated log files to keep, by default 5.
    propagate : bool, optional
        Whether to propagate logs to parent loggers, by default True.
        Set to False to isolate this logger from the root logger, preventing records from being
        handled by any ancestor loggers.
    output_console : bool, optional
        Whether to output logs to console, by default True.
    colored_console : bool, optional
        Use colors in the console output, by default True.
    output_format : str, optional
        Format string for log messages, by default:
        ``"%(asctime)s - %(name)s - %(levelname)s - %(message)s"``.

    Returns
    -------
    logging.Logger
        Configured logger instance.

    Raises
    ------
    ValueError
        If an invalid logging level is provided.

    Examples
    --------
    Configure the root logger (recommended for most applications):

        >>> logger = init_logger()

    Configure a named logger with per-handler levels:

        >>> logger = init_logger(
        ...     name="myapp",
        ...     level="DEBUG",
        ...     level_file="WARNING",
        ...     output_folder=Path("logs"),
        ...     propagate=True,
        ... )
        >>> child = logging.getLogger("myapp.module")  # inherits myapp's handlers
    """
    if level_file is not None and output_folder is None:
        warnings.warn(
            "`level_file` is set but `output_folder` is None — file handler will not be created"
            " and `level_file` has no effect.",
            UserWarning,
            stacklevel=2,
        )

    logger = logging.getLogger(name)

    # Clear handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    try:
        level = _set_level(level)
        level_console = _set_level(level_console, default_level=level)
        level_file = _set_level(level_file, default_level=level)
    except (ValueError, TypeError) as e:
        error_msg = f"Invalid logging level: {e!s}"
        raise ValueError(error_msg) from e

    logger.setLevel(logging.DEBUG)
    logger.propagate = propagate

    formatter = logging.Formatter(output_format)

    if output_folder is not None:
        create_folder(output_folder, includes_file=False)
        timestamp = datetime.now(tz=UTC).astimezone().strftime("%Y%m%d_%H%M%S")
        safe_name = name or "root"
        log_file = output_folder / f"{safe_name}_{timestamp}.log"

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file, maxBytes=file_size, backupCount=backup_count
        )
        file_handler.setLevel(level_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if output_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level_console)
        if colored_console:
            console_handler.setFormatter(ColorFormatter(output_format))
        else:
            console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if not logger.handlers:
        warnings.warn(
            f"Logger {name!r} has no handlers configured. All log records will be silently"
            " discarded.",
            UserWarning,
            stacklevel=2,
        )

    if name and not propagate:
        warnings.warn(
            f"Logger {name!r} has propagate=False. Child loggers will not inherit this"
            " configuration.",
            UserWarning,
            stacklevel=2,
        )

    return logger


def setup_null_handler(name: str) -> None:
    """Set up a NullHandler for a library logger.

    This is the correct way to configure logging in a reusable library or sub-package. It registers
    the logger under the given name without attaching any real handler, ensuring the library stays
    silent by default and lets the consuming application decide where and how logs are routed.

    Call this once in the top-level ``__init__.py`` of your library:

    .. code-block:: python

        from pyauxlib.utils.logger import setup_null_handler

        setup_null_handler(__name__)

    Any module within the library should then obtain its logger via:

    .. code-block:: python

        import logging

        logger = logging.getLogger(__name__)

    Parameters
    ----------
    name : str
        Name of the library's root logger, typically ``__name__`` of the package's
        ``__init__.py`` (e.g. ``"mylib"``).

    Notes
    -----
    Do **not** call :func:`init_logger` inside a library. That function is intended for
    application-level configuration only. Calling it inside a library would either silence
    propagation to the parent application (``propagate=False``) or produce duplicate output
    (``propagate=True``).
    """
    logging.getLogger(name).addHandler(logging.NullHandler())

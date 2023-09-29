"""Module providing the Timer class for measuring and logging execution times."""
import csv
import io
import logging
import time
import warnings
from pathlib import Path
from typing import ClassVar, Protocol, Self

import wrapt


class TimeFunc(Protocol):
    """Protocol for functions that return the current time as a float."""

    def __call__(self) -> float:
        """Get the current time.

        Returns
        -------
        float
            The current time.
        """
        ...


class Timer:
    """Timer class to measure execution times.

    The timer can be managed in three ways:

    1. Manually, by calling the `start`, `stop`, etc. methods.
    2. As a context manager, which automatically starts the timer when entering the context and
    stops it when exiting.
    3. As a decorator, which times the execution of the decorated function.

    Parameters
    ----------
    filename : str | Path | None
        The name or path of the file to save the timestamps.
    time_func : {"time", "perf_counter", "process_time"} | callable, optional
        The time function to use. It can be one of {"time", "perf_counter",
        "process_time"} or a custom time function. By default "time".
    logger : logging.Logger, optional
        The logger to use for logging warnings. By default None.

    Attributes
    ----------
    filename : str | Path | None
        The name of the file to save the timestamps. By default None.
    start_time : float or None
        The start time of the timer.
    stop_time : float or None
        The stop time of the timer.
    timestamps : list of float
        The list of timestamps added during the timer execution.
    texts : list of str
        The list of texts associated with each timestamp.

    Examples
    --------
    Example usage:

    ```python
    # Manual usage
    t = Timer()
    t.start()
    # code here
    t.stop()

    # Context manager usage
    with Timer() as t:
        # code here
        t.add_timestamp("#1")
        # more code
        # The timer will automatically be stopped when exiting the context manager

    # Decorator usage
    timer = Timer()
    @timer
    def some_function():
        # function code
    ```
    """

    TIME_FUNC: ClassVar[dict[str, TimeFunc]] = {
        "time": time.time,
        "perf_counter": time.perf_counter,
        "process_time": time.process_time,
    }

    def __init__(
        self,
        filename: str | Path | None = None,
        time_func: str | TimeFunc = "time",
        logger: logging.Logger | None = None,
    ):
        self.filename = Path(filename) if filename is not None else None

        if isinstance(time_func, str):
            self.time_func = self.TIME_FUNC[time_func]
        else:
            self.time_func = time_func

        self.logger = warnings.warn if logger is None else logger.warning
        self.where_output = None if logger is None else logger.info
        self.running = False
        self.reset()

    def __enter__(self) -> Self:
        """Start a new timer as a context manager."""
        self.start()
        return self

    def __exit__(self, *exc_info: object):
        """Stop the context manager timer."""
        self.stop()

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        """Measure the execution time of a decorated function or method."""
        self.start()
        result = wrapped(*args, **kwargs)
        self.stop()
        return result

    def start(self):
        """Start the timer."""
        if self.stop_time is not None:
            self.logger("Timer has not been resetted.")
            return
        self.running = True
        self.add_timestamp("start")
        self.start_time = self.timestamps[-1]

    def stop(self) -> float:
        """Stop the timer and returns the ellapsed time.

        It also saves the timestamps to a file, when provided.
        """
        if self.start_time is None:
            self.logger("Timer has not been started.")
            return 0

        self.add_timestamp("stop")
        self.stop_time = self.timestamps[-1]
        self.running = False
        self.save()

        ellapsed_time = self.stop_time - self.start_time

        if self.where_output is not None:
            self.where_output(f"Ellapsed time: {ellapsed_time} s")

        return ellapsed_time

    def add_timestamp(self, text=""):
        """Add a timestamp with an associated text.

        Parameters
        ----------
        text : str, optional
            The text associated with the timestamp. By default "".
        """
        if not self.running:
            self.logger("Timer is not running.")

        self.timestamps.append(self.time_func())
        self.texts.append(text)

    def save(self, filename: str | Path | None = None):
        """Save the timestamps and their associated texts to a file.

        Parameters
        ----------
        filename : str | Path | None, optional
            The name or path of the file to save the timestamps to. If not provided,
            the filename attribute of the Timer object will be used. By default None.
        """
        if self.start_time is None:
            self.logger("Timer has not been started.")
            return
        if self.stop_time is None:
            self.logger("Timer has not been stopped yet.")
            return
        if (filename := filename or self.filename) is None:
            return

        filename = Path(filename)

        with Path.open(filename, "w", newline="") as csvfile:
            csvfile.write(self._to_csv())

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.stop_time = None
        self.timestamps = []
        self.texts = []

    def get_data(self) -> list[list[str]]:
        """Get the timer data as a list of rows.

        This method returns the timer data, including the comment, timestamp, time,
        step time, and accumulated time for each timestamp, as a list of rows. The
        first row is the header.

        Returns
        -------
        list of list of str
            The timer data. Each inner list represents a row. The first row is the
            header.
        """
        rows = []
        header = ["Comment", "Timestamp", "Time", "Step Time", "Accumulated Time"]
        rows.append(header)

        prev_time = self.start_time
        for i, timestamp in enumerate(self.timestamps):
            elapsed_time = timestamp - prev_time
            total_time = timestamp - self.start_time
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            row = [
                self.texts[i],
                str(timestamp),
                formatted_time,
                str(elapsed_time),
                str(total_time),
            ]
            rows.append(row)
            prev_time = timestamp

        return rows

    def _to_csv(self):
        rows = self.get_data()

        # Convert rows to CSV string
        csv_str = io.StringIO()
        writer = csv.writer(csv_str)
        writer.writerows(rows)
        return csv_str.getvalue()

    def __str__(self) -> str:
        """Get the timer data as a printable string."""
        rows = self.get_data()

        # Compute column widths
        col_widths = [max(len(cell) for cell in col) for col in zip(*rows, strict=True)]

        # Format rows as table
        table_rows = []
        for row in rows:
            table_row = "  ".join(
                cell.ljust(width) for cell, width in zip(row, col_widths, strict=True)
            )
            table_rows.append(table_row)

        return "\n".join(table_rows)

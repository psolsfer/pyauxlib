"""Unicode symbol constants, organized by category as ``StrEnum`` subclasses.

Enum members behave as standard strings, allowing direct comparison, formatting, and concatenation
without explicit ``.value`` access.

Examples
--------
>>> MathSymbol.TIMES in "3 × 4"
True
>>> f"Tolerance {MathSymbol.GEQ} 0.01"
'Tolerance ≥ 0.01'
"""

import unicodedata
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from strenum import StrEnum
else:
    try:
        from enum import StrEnum
    except ImportError:  # Python < 3.11
        from strenum import StrEnum


# ruff: noqa: RUF001, RUF002


@dataclass(frozen=True)
class SymbolInfo:
    """Information about a given symbol."""

    name: str
    value: str
    unicode: str
    description: str


class Symbol(StrEnum):
    """Base enum class for categorized Unicode symbols."""

    @property
    def info(self) -> SymbolInfo:
        """Return metadata describing this Unicode symbol."""
        return SymbolInfo(
            name=self.name,
            value=self.value,
            unicode=f"U+{ord(self):04X}",
            description=unicodedata.name(self, ""),
        )

    @classmethod
    def items(cls) -> list[SymbolInfo]:
        """Return metadata for all symbols defined in the enum."""
        return [member.info for member in cls.__members__.values()]

    @classmethod
    def values(cls) -> list[str]:
        """Return the raw Unicode character values of all symbols."""
        return [member.value for member in cls.__members__.values()]

    @classmethod
    def names(cls) -> list[str]:
        """Return the enum member names for all symbols."""
        return [member.name for member in cls.__members__.values()]


class TypoSymbol(Symbol):
    """Typographic and punctuation symbols."""

    ELLIPSIS = "…"  # \u2026
    EM_DASH = "—"  # \u2014
    BULLET = "●"  # \u25cf
    DEGREE = "°"  # \u00b0
    QUOTE_LEFT = "‘"  # \u2018
    QUOTE_RIGHT = "’"  # \u2019


class MathSymbol(Symbol):
    """Mathematical operators and relations."""

    MINUS = "−"  # \u2212
    PLUS_MINUS = "±"  # \u00b1
    TIMES = "×"  # \u00d7
    SQRT = "√"  # \u221a
    GEQ = "≥"  # \u2265
    SQUARED = "²"  # \u00b2
    JOINED_SQUARES = "⧉"  # \u29c9
    PROPORTIONAL_TO = "∝"  # \u221d


class ArrowSymbol(Symbol):
    """Arrows and directional indicators."""

    RIGHT = "→"  # \u2192
    RIGHT_SMALL = "▸"  # \u25b8
    DOWN_SMALL = "▾"  # \u25be
    POINTER_RIGHT = "☞"  # \u261e


class GreekSymbol(Symbol):
    """Greek letters."""

    SIGMA = "σ"  # \u03c3


class IconSymbol(Symbol):
    """Emoji and icon symbols."""

    LIGHT_BULB = "💡"  # \U0001f4a1

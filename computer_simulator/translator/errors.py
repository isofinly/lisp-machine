from __future__ import annotations

from typing import Any


class InvalidSymbolsError(Exception):
    def __init__(self, got: Any, expected: Any) -> None:
        self.token = got
        self.expected = expected

    def __str__(self) -> str:
        return f"Got invalid symbols or tokens: {self.token}, expected: {self.expected}"

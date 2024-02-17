from typing import Any


def safe_int(value: Any | None) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_float(value: Any | None) -> float | None:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

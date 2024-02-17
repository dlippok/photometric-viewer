def safe_int(value: str | None) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def safe_float(value: str | None) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

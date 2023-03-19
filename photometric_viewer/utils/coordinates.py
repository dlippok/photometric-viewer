from typing import Tuple


def cartesian_to_screen(center: Tuple[int, int], point: Tuple[int, int]) -> Tuple[int, int]:
    return center[0] + point[0], center[1] - point[1]
from typing import Tuple


def cartesian_to_screen(center: Tuple[float, float], point: Tuple[float, float]) -> Tuple[float, float]:
    return center[0] + point[0], center[1] - point[1]
    
def screen_to_cartesian(center: Tuple[float, float], point: Tuple[float, float]) -> Tuple[float, float]:
    return point[0] - center[0], point[1] - center[1] 

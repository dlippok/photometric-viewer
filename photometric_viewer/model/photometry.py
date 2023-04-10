from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, List


@dataclass
class PhotometryMetadata:
    luminaire: str
    manufacturer: str
    additional_properties: Dict[str, str]


class LuminousOpeningShape(Enum):
    RECTANGULAR = 1
    ROUND = 2

@dataclass
class LuminousOpening:
    width: float
    length: float
    shape: LuminousOpeningShape


@dataclass
class Photometry:
    lumens: float
    v_angles: List[float]
    h_angles: List[float]
    c_values: Dict[Tuple[float, float], float]
    luminous_opening: LuminousOpening
    metadata: PhotometryMetadata

    def get_values_for_c_angle(self, angle) -> Dict[float, float]:
        if angle in self.h_angles:
            return self._values_for_angle(angle)
        elif angle < 180 and angle + 180 in self.h_angles:
            return self._values_for_angle(angle + 180)
        elif angle >= 180 and angle - 180 in self.h_angles:
            return self._values_for_angle(angle - 180)
        else:
            return {}

    def _values_for_angle(self, angle):
        return {
            angles[1]: candelas
            for (angles, candelas) in self.c_values.items()
            if angles[0] == angle

        }

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, List

from photometric_viewer.model.units import LengthUnits


@dataclass
class PhotometryMetadata:
    luminaire: str
    catalog_number: str
    manufacturer: str
    additional_properties: Dict[str, str]
    file_source: str
    file_units: LengthUnits


class Shape(Enum):
    RECTANGULAR = 1
    ROUND = 2


@dataclass
class LuminousOpeningGeometry:
    width: float
    length: float
    shape: Shape


@dataclass
class LuminaireGeometry:
    width: float
    length: float
    height: float
    shape: Shape


@dataclass
class Lamps:
    number_of_lamps: int
    is_absolute: bool
    description: str | None = None
    catalog_number: str | None = None
    position: str | None = None
    lumens_per_lamp: float | None = None
    wattage: float | None = None
    color: str | None = None
    cri: int | None = None
    ballast_description: str | None = None
    ballast_catalog_number: str | None = None


@dataclass
class Photometry:
    is_absolute: bool
    v_angles: List[float]
    h_angles: List[float]

    # Values in Candela for absolute photometry, cd/klm otherwise
    c_values: Dict[Tuple[float, float], float]
    dff: float | None
    lorl: float | None
    luminous_opening_geometry: LuminousOpeningGeometry
    luminaire_geometry: LuminaireGeometry | None
    lamps: List[Lamps]
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

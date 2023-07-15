from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, List

from photometric_viewer.model.units import LengthUnits


class LuminaireType(Enum):
    POINT_SOURCE_WITH_VERTICAL_SYMMETRY = 1
    LINEAR = 2
    POINT_SOURCE_WITH_OTHER_SYMMETRY = 3


@dataclass
class PhotometryMetadata:
    luminaire: str
    catalog_number: str
    manufacturer: str
    additional_properties: Dict[str, str]
    file_source: str
    file_units: LengthUnits
    luminaire_type: LuminaireType | None = None
    measurement: str | None = None
    date_and_user: str | None = None
    conversion_factor: float | None = None
    filename: str | None = None


class Shape(Enum):
    RECTANGULAR = 1
    ROUND = 2


class LuminousOpeningShape(Enum):
    POINT = 1
    RECTANGULAR = 2
    ROUND = 3
    SPHERE = 4
    HORIZONTAL_CYLINDER_ALONG_LENGTH = 5
    HORIZONTAL_CYLINDER_ALONG_WIDTH = 6
    ELLIPSE_ALONG_LENGTH = 7
    ELLIPSE_ALONG_WIDTH = 8
    ELLIPSOID_ALONG_LENGTH = 9
    ELLIPSOID_ALONG_WIDTH = 10


@dataclass
class LuminousOpeningGeometry:
    width: float
    length: float
    height: float
    shape: LuminousOpeningShape
    height_c90: float | None = None
    height_c180: float | None = None
    height_c270: float | None = None


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
    gamma_angles: List[float]
    c_planes: List[float]

    # Values in Candela for absolute photometry, cd/klm otherwise
    intensity_values: Dict[Tuple[float, float], float]
    dff: float | None
    lorl: float | None
    luminous_opening_geometry: LuminousOpeningGeometry
    luminaire_geometry: LuminaireGeometry | None
    lamps: List[Lamps]
    metadata: PhotometryMetadata

    def get_values_for_c_angle(self, angle) -> Dict[float, float]:
        if angle in self.c_planes:
            return self._values_for_angle(angle)
        elif angle < 180 and angle + 180 in self.c_planes:
            return self._values_for_angle(angle + 180)
        elif angle >= 180 and angle - 180 in self.c_planes:
            return self._values_for_angle(angle - 180)
        else:
            return {}

    def _values_for_angle(self, angle):
        return {
            angles[1]: candelas
            for (angles, candelas) in self.intensity_values.items()
            if angles[0] == angle

        }

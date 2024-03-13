from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Tuple, List, Any

from photometric_viewer.model.units import LengthUnits


class LuminaireType(Enum):
    POINT_SOURCE_WITH_VERTICAL_SYMMETRY = 1
    LINEAR = 2
    POINT_SOURCE_WITH_OTHER_SYMMETRY = 3


class Symmetry(Enum):
    NONE = 0
    TO_VERTICAL_AXIS = 1
    TO_C0_C180 = 2
    TO_C90_C270 = 3
    TO_C0_C180_C90_C270 = 4


class FileFormat(Enum):
    IES = 1
    LDT = 2


@dataclass
class PhotometryMetadata:
    luminaire: str | None = None
    catalog_number: str | None = None
    manufacturer: str | None = None
    file_source: str | None = None
    file_units: LengthUnits = LengthUnits.METERS
    luminaire_type: LuminaireType | None = None
    measurement: str | None = None
    date_and_user: str | None = None
    conversion_factor: float | None = None
    filename: str | None = None
    additional_properties: Dict[str, str] = field(default_factory=dict)
    symmetry: Symmetry = Symmetry.NONE
    direct_ratios_for_room_indices: Dict[float, float] = field(default_factory=dict)
    file_format: FileFormat | None = None

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
    shape: LuminousOpeningShape | None
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
    number_of_lamps: int | None
    description: str | None = None
    catalog_number: str | None = None
    position: str | None = None
    lumens_per_lamp: float | None = None
    wattage: float | None = None
    color: str | None = None
    cri: str | None = None
    ballast_description: str | None = None
    ballast_catalog_number: str | None = None


@dataclass
class Calculable:
    value: Any | None = None
    is_calculated: bool = False

    def to_calculated(self, value: Any):
        if self.value is None and value is not None:
            return Calculable(value, True)
        else:
            return self

    def from_percent(self):
        if self.value is None:
            return Calculable(None, self.is_calculated)
        return Calculable(self.value / 100, self.is_calculated)


@dataclass()
class LuminairePhotometricProperties:
    is_absolute: bool = False
    luminous_flux: Calculable = field(default_factory=Calculable)
    efficacy: Calculable = field(default_factory=Calculable)
    lor: Calculable = field(default_factory=Calculable)
    dff: Calculable = field(default_factory=Calculable)

    def get(self):
        return self.luminous_flux

@dataclass
class Luminaire:
    gamma_angles: List[float] = field(default_factory=list)
    c_planes: List[float] = field(default_factory=list)
    # Values in Candela for absolute photometry, cd/klm otherwise
    intensity_values: Dict[Tuple[float, float], float] = field(default_factory=dict)
    luminous_opening_geometry: LuminousOpeningGeometry | None = None
    geometry: LuminaireGeometry | None = None
    lamps: List[Lamps] = field(default_factory=list)
    metadata: PhotometryMetadata = field(default_factory=PhotometryMetadata)

    photometry: LuminairePhotometricProperties
    _photometry: LuminairePhotometricProperties = field(init=False, repr=False)

    @property
    def photometry(self) -> LuminairePhotometricProperties:
        return self._photometry

    @photometry.setter
    def photometry(self, value: LuminairePhotometricProperties):
        self._photometry = value

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

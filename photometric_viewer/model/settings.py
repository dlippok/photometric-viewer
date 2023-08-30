from dataclasses import dataclass
from enum import Enum

from photometric_viewer.model.units import LengthUnits

class DiagramStyle(Enum):
    SIMPLE = 1
    DETAILED = 2


class SnapValueAnglesTo(Enum):
    MAX_VALUE = 1
    ROUND_NUMBER = 2


class DisplayHalfSpaces(Enum):
    BOTH = 1
    ONLY_RELEVANT = 2


@dataclass
class Settings:
    length_units_from_file: bool = False
    length_units: LengthUnits | None = LengthUnits.METERS
    electricity_price_per_kwh: float = 0.25
    diagram_style: DiagramStyle = DiagramStyle.SIMPLE
    snap_value_angles_to: SnapValueAnglesTo = SnapValueAnglesTo.MAX_VALUE
    display_half_spaces: DisplayHalfSpaces = DisplayHalfSpaces.ONLY_RELEVANT
    diagram_theme: str | None = None

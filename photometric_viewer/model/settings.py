from dataclasses import dataclass

from photometric_viewer.model.units import LengthUnits


@dataclass
class Settings:
    length_units_from_file: bool
    length_units: LengthUnits | None

from dataclasses import dataclass, field
from typing import List


@dataclass
class LampSet:
    number_of_lamps: int | None = None
    type_of_lamp: str | None = None
    total_lumens: float | None = None
    light_color: str | None = None
    cri: int | None = None
    wattage: float | None = None


@dataclass
class LdtContent:
    header: str | None = None
    type_indicator: int | None = None
    symmetry_indicator: int | None = None
    number_of_c_planes: int | None = None
    distance_between_c_planes: float | None = None
    number_of_intensities: int | None = None
    distance_between_intensities: float | None = None
    measurement_report: str | None = None
    luminaire_name: str | None = None
    luminaire_number: str | None = None
    file_name: str | None = None
    date_and_user: str | None = None
    length_of_luminaire: float | None = None
    width_of_luminaire: float | None = None
    height_of_luminaire: float | None = None
    length_of_luminous_area: float | None = None
    width_of_luminous_area: float | None = None
    height_of_luminous_area_c0: float | None = None
    height_of_luminous_area_c90: float | None = None
    height_of_luminous_area_c180: float | None = None
    height_of_luminous_area_c270: float | None = None
    dff_percent: float | None = None
    lor_percent: float | None = None
    conversion_factor: float | None = None
    tilt: float | None = None
    number_of_lamp_sets: int | None = None
    lamp_sets: List[LampSet] = field(default_factory=list)
    direct_ratios_for_room_indices: List[float] = field(default_factory=list)
    c_angles: List[float] = field(default_factory=list)
    gamma_angles: List[float] = field(default_factory=list)
    intensities: List[float] = field(default_factory=list)

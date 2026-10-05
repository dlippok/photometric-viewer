from dataclasses import dataclass, field
from typing import Any, List

from photometric_viewer.photometry.common import Attribute

@dataclass
class LampSet:
    number_of_lamps: Attribute
    type_of_lamp: Attribute
    total_lumens: Attribute
    light_color: Attribute
    cri: Attribute
    wattage: Attribute

@dataclass
class LdtContent:
    header: Attribute
    type_indicator: Attribute
    symmetry_indicator: Attribute
    number_of_c_planes: Attribute
    distance_between_c_planes: Attribute
    number_of_intensities: Attribute
    distance_between_intensities: Attribute
    measurement_report: Attribute
    luminaire_name: Attribute
    luminaire_number: Attribute
    file_name: Attribute
    date_and_user: Attribute
    length_of_luminaire: Attribute
    width_of_luminaire: Attribute
    height_of_luminaire: Attribute
    length_of_luminous_area: Attribute
    width_of_luminous_area: Attribute
    height_of_luminous_area_c0: Attribute
    height_of_luminous_area_c90: Attribute
    height_of_luminous_area_c180: Attribute
    height_of_luminous_area_c270: Attribute
    dff_percent: Attribute
    lor_percent: Attribute
    conversion_factor: Attribute
    tilt: Attribute
    number_of_lamp_sets: Attribute
    lamp_sets: List[LampSet] = field(default_factory=list)
    direct_ratios_for_room_indices: List[Attribute] = field(default_factory=list)
    c_angles: List[Attribute] = field(default_factory=list)
    gamma_angles: List[Attribute] = field(default_factory=list)
    intensities: List[Attribute] = field(default_factory=list)


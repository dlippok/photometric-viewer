from dataclasses import dataclass, field
from typing import List


@dataclass
class Attribute:
    value: str | None
    line: int # Actual line or expected line number if the value is missing


@dataclass
class InlineAttributes:
    number_of_lamps: Attribute
    lumens_per_lamp: Attribute
    multiplying_factor: Attribute
    n_v_angles: Attribute
    n_h_angles: Attribute
    photometry_type: Attribute
    luminous_opening_units: Attribute
    luminous_opening_width: Attribute
    luminous_opening_length: Attribute
    luminous_opening_height: Attribute


@dataclass
class LampAttributes:
    ballast_factor: Attribute
    ballast_lamp_photometric_factor: Attribute
    input_watts: Attribute


@dataclass
class MetadataTuple:
    key: str
    value: str
    line: int


@dataclass
class IesContent:
    header: str | None = None
    metadata: List[MetadataTuple] = field(default_factory=list)
    inline_attributes: InlineAttributes = field(default_factory=lambda: InlineAttributes())
    lamp_attributes: LampAttributes = field(default_factory=lambda: LampAttributes())
    v_angles: List[Attribute] = field(default_factory=list)
    h_angles: List[Attribute] = field(default_factory=list)
    intensities: List[Attribute] = field(default_factory=list)
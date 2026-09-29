from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Attribute:
    value: str
    line: int


@dataclass
class InlineAttributes:
    number_of_lamps: Attribute | None = None
    lumens_per_lamp: Attribute | None = None
    multiplying_factor: Attribute | None = None
    n_v_angles: Attribute | None = None
    n_h_angles: Attribute | None = None
    photometry_type: Attribute | None = None
    luminous_opening_units: Attribute | None = None
    luminous_opening_width: Attribute | None = None
    luminous_opening_length: Attribute | None = None
    luminous_opening_height: Attribute | None = None


@dataclass
class LampAttributes:
    ballast_factor: Attribute | None = None
    ballast_lamp_photometric_factor: Attribute | None = None
    input_watts: Attribute | None = None


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
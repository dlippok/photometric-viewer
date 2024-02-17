from dataclasses import dataclass
from typing import List


@dataclass
class InlineAttributes:
    number_of_lamps : int | None
    lumens_per_lamp: float | None
    multiplying_factor: float | None
    n_v_angles: int | None
    n_h_angles: int | None
    photometry_type: int | None
    luminous_opening_units: int | None
    luminous_opening_width: int | None
    luminous_opening_length: int | None
    luminous_opening_height: int | None


@dataclass
class LampAttributes:
    ballast_factor: float | None
    photometric_factor: float | None
    input_watts: float | None


@dataclass
class MetadataTuple:
    key: str
    value: str


@dataclass
class IesContent:
    header: str | None
    metadata: List[MetadataTuple]
    inline_attributes: InlineAttributes
    lamp_attributes: LampAttributes
    v_angles: List[float] | None
    h_angles: List[float] | None
    intensities: List[float]
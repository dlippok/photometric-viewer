from dataclasses import dataclass, field
from typing import List


@dataclass
class InlineAttributes:
    number_of_lamps : int | None = None
    lumens_per_lamp: float | None = None
    multiplying_factor: float | None = None
    n_v_angles: int | None = None
    n_h_angles: int | None = None
    photometry_type: int | None = None
    luminous_opening_units: int | None = None
    luminous_opening_width: float | None = None
    luminous_opening_length: float | None = None
    luminous_opening_height: float | None = None


@dataclass
class LampAttributes:
    ballast_factor: float | None = None
    future_use: str | None = None
    input_watts: float | None = None


@dataclass
class MetadataTuple:
    key: str
    value: str


@dataclass
class IesContent:
    header: str | None = None
    metadata: List[MetadataTuple] = field(default_factory=list)
    inline_attributes: InlineAttributes = field(default_factory=lambda: InlineAttributes())
    lamp_attributes: LampAttributes = field(default_factory=lambda: LampAttributes())
    v_angles: List[float | None] = field(default_factory=list)
    h_angles: List[float | None] = field(default_factory=list)
    intensities: List[float] = field(default_factory=list)
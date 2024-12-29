import dataclasses


@dataclasses.dataclass
class ZoneProperties:
    width: float
    length: float
    target_illuminance: float
    maintenance_factor: float

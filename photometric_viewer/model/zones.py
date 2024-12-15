import dataclasses


@dataclasses.dataclass
class ZoneProperties:
    width: float
    height: float
    target_illuminance: float
    maintenance_factor: float

import dataclasses


@dataclasses.dataclass
class RoomProperties:
    width: float
    height: float
    target_illuminance: float
    maintenance_factor: float

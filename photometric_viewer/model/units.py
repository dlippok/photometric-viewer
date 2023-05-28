from enum import Enum

M_IN_FEET = 0.3048


class LengthUnits(Enum):
    METERS = 1
    CENTIMETERS = 2
    MILLIMETERS = 3
    FEET = 4
    INCHES = 5


def length_factor(units: LengthUnits):
    match units:
        case LengthUnits.METERS:
            return 1
        case LengthUnits.CENTIMETERS:
            return 100
        case LengthUnits.MILLIMETERS:
            return 1000
        case LengthUnits.FEET:
            return 3.2808
        case LengthUnits.INCHES:
            return 39.3701

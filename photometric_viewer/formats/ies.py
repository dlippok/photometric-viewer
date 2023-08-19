from typing import IO

from photometric_viewer.formats.exceptions import InvalidLuminousOpeningException, InvalidPhotometricFileFormatException
from photometric_viewer.model.photometry import Photometry, PhotometryMetadata, LuminousOpeningGeometry, Shape, \
    Lamps, LuminousOpeningShape
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.utils.io import read_non_empty_line


def _get_n_values(f: IO, n: int):
    raw_values = []
    while n > 0:
        line = read_non_empty_line(f)
        if line.strip() == "":
            continue

        values = line.strip().split(" ")
        for value in values:
            if value == "":
                continue
            raw_values.append(value)
            n -= 1
    return raw_values


def create_luminous_opening(attributes):
    f = 0 # Factor for unit conversion (internally always stored in meters)
    match attributes["luminous_opening_units"]:
        case 1:
            f = 0.3048
        case 2:
            f = 1

    match (
        attributes["luminous_opening_width"],
        attributes["luminous_opening_length"],
        attributes["luminous_opening_height"]
    ):
        case 0, 0, 0:
            return LuminousOpeningGeometry(0, 0, 0, shape=LuminousOpeningShape.POINT)
        case w, l, h if w > 0 and l > 0 and h >= 0:
            return LuminousOpeningGeometry(w * f, l * f, h * f, LuminousOpeningShape.RECTANGULAR)
        case w, l, h if w > 0 and l == 0 and h >= 0:
            return LuminousOpeningGeometry(w * f, w * f, h * f, LuminousOpeningShape.RECTANGULAR)
        case w, l, h if w == 0 and l > 0 and h >= 0:
            return LuminousOpeningGeometry(l * f, l * f, h * f, LuminousOpeningShape.RECTANGULAR)
        case w, l, h if w < 0 and l < 0 and h >= 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, h * f, LuminousOpeningShape.ROUND)
        case w, l, h if w < 0 and l == 0 and h >= 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(w) * f, h * f, LuminousOpeningShape.ROUND)
        case w, l, h if w == 0 and l < 0 and h >= 0:
            return LuminousOpeningGeometry(abs(l) * f, abs(l) * f, h * f, LuminousOpeningShape.ROUND)
        case w, 0, h if w == h and w < 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(w) * f, abs(w) * f, LuminousOpeningShape.SPHERE)
        case 0, l, h if l > 0 and h < 0:
            return LuminousOpeningGeometry(abs(l) * f, abs(l) * f, abs(h) * f, LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH)
        case w, 0, h if w > 0 and h < 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(w) * f, abs(h) * f, LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH)
        case w, l, h if w < 0 and l > 0 and h > 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f, LuminousOpeningShape.ELLIPSE_ALONG_LENGTH)
        case w, l, h if w > 0 and l < 0 and h > 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f, LuminousOpeningShape.ELLIPSE_ALONG_WIDTH)
        case w, l, h if w < 0 and l > 0 and h < 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f, LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH)
        case w, l, h if w > 0 and l < 0 and h < 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f, LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH)
        case _:
            raise InvalidLuminousOpeningException()


def import_from_file(f: IO):
    header = read_non_empty_line(f).strip()
    if not header.upper().startswith("IESNA"):
        raise InvalidPhotometricFileFormatException(f"{header} could not be recognized as a valid IESNA file header")

    metadata = {}
    next_line = read_non_empty_line(f)
    last_key = None
    while next_line.startswith("["):
        metadata_line = next_line.split("]")
        metadata_key = metadata_line[0].strip("[").strip()
        metadata_value = metadata_line[1].strip()
        if metadata_key == 'MORE' and last_key is not None:
            metadata[last_key] = metadata[last_key] + "\n" + metadata_value
        elif metadata_key in metadata.keys():
            metadata[metadata_key] = metadata[metadata_key] + "\n" + metadata_value
            last_key = metadata_key
        else:
            metadata[metadata_key] = metadata_value
            last_key = metadata_key
        next_line = read_non_empty_line(f)

    raw_attributes = _get_n_values(f, 10)
    attributes = {
        "numer_of_lamps": int(raw_attributes[0]),
        "lumens_per_lamp": float(raw_attributes[1]),
        "multiplying_factor": float(raw_attributes[2]),
        "n_v_angles": int(raw_attributes[3]),
        "n_h_angles": int(raw_attributes[4]),
        "photometer_type": int(raw_attributes[5]),
        "luminous_opening_units": int(raw_attributes[6]),
        "luminous_opening_width": float(raw_attributes[7]),
        "luminous_opening_length": float(raw_attributes[8]),
        "luminous_opening_height": float(raw_attributes[9]),
    }

    [ballast_factor, lamp_photometric_factor, input_watts] = _get_n_values(f, 3)

    v_angles = [float(angle) for angle in _get_n_values(f, attributes["n_v_angles"])]
    h_angles = [float(angle) for angle in _get_n_values(f, attributes["n_h_angles"])]

    raw_values = _get_n_values(f, attributes["n_v_angles"] * attributes["n_h_angles"])

    lumens = attributes["lumens_per_lamp"] * attributes["numer_of_lamps"] if attributes[
                                                                                 "lumens_per_lamp"] >= 0 else None

    candela_values = {}
    relative_photomety_divider = lumens / 1000 if lumens else 1
    n = 0
    for h_angle in h_angles:
        for v_angle in v_angles:
            raw_value = float(raw_values[n])
            multiplying_factor = attributes["multiplying_factor"]
            value = raw_value * multiplying_factor * float(ballast_factor) * float(lamp_photometric_factor)
            candela_values[(h_angle, v_angle)] = round(value / relative_photomety_divider, ndigits=2)
            n += 1

    f.seek(0)
    source = f.read()

    return Photometry(
        is_absolute=lumens is None,
        gamma_angles=v_angles,
        c_planes=h_angles,
        intensity_values=candela_values,
        luminous_opening_geometry=create_luminous_opening(attributes),
        luminaire_geometry=None,
        dff=None,
        lorl=None,
        lamps=[Lamps(
            number_of_lamps=attributes["numer_of_lamps"],
            lumens_per_lamp=attributes["lumens_per_lamp"] if attributes["lumens_per_lamp"] >= 0 else None,
            is_absolute=attributes["lumens_per_lamp"] < 0,
            description=metadata.pop("LAMP", None),
            catalog_number=metadata.pop("LAMPCAT", None),
            position=metadata.pop("LAMPPOSITION", None),
            ballast_catalog_number=metadata.pop("BALLASTCAT", None),
            ballast_description=metadata.pop("BALLAST", None),
            wattage=None,
            color=None,
            cri=None,
        )],
        metadata=PhotometryMetadata(
            catalog_number=metadata.pop("LUMCAT", None),
            luminaire=metadata.pop("LUMINAIRE", None),
            manufacturer=metadata.pop("MANUFAC", None),
            date_and_user=metadata.pop("ISSUEDATE", None),
            additional_properties=metadata,
            file_source=source,
            file_units=LengthUnits.FEET if attributes["luminous_opening_units"] == 1 else LengthUnits.METERS
        )
    )


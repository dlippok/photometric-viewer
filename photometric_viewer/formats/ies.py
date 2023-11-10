import datetime
from typing import IO, Dict

from photometric_viewer.formats.exceptions import InvalidLuminousOpeningException, InvalidPhotometricFileFormatException
from photometric_viewer.model.luminaire import Luminaire, PhotometryMetadata, LuminousOpeningGeometry, Shape, \
    Lamps, LuminousOpeningShape, LuminairePhotometricProperties, Calculable
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.utils.ioutil import read_non_empty_line

_LUMEN_PER_LAMPS_ABSOLUTE = -1
_LUMEN_PER_LAMPS_1000 = 1000

_DEFAULT_MULTIPLIER = 1.0
_PHOTOMETRIC_TYPE_C = 1
_UNIT_TYPE_FEET = 1
_UNIT_TYPE_METERS = 2
_DEFAULT_BALLAST_FACTOR = 1.0
_FUTURE_USE = 1

_VALUES_PER_LINE = 12

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


def create_luminous_opening_for_iesna95(w, l, h, f):
    match (w, l, h):
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
            return LuminousOpeningGeometry(abs(l) * f, abs(l) * f, abs(h) * f,
                                           LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH)
        case w, 0, h if w > 0 and h < 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(w) * f, abs(h) * f,
                                           LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH)
        case w, l, h if w < 0 and l > 0 and h > 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f,
                                           LuminousOpeningShape.ELLIPSE_ALONG_LENGTH)
        case w, l, h if w > 0 and l < 0 and h > 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f, LuminousOpeningShape.ELLIPSE_ALONG_WIDTH)
        case w, l, h if w < 0 and l > 0 and h < 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f,
                                           LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH)
        case w, l, h if w > 0 and l < 0 and h < 0:
            return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f,
                                           LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH)
        case _:
            raise InvalidLuminousOpeningException()

def create_luminous_opening_for_iesna02(w, l, h, f):
    if w == 0 and l == 0 and h == 0:
        shape = LuminousOpeningShape.POINT
    elif w > 0 and l > 0 and h == 0:
        shape = LuminousOpeningShape.RECTANGULAR
    elif w > 0 and l > 0 and h > 0:
        shape = LuminousOpeningShape.RECTANGULAR
    elif w < 0 and l < 0 and h >= 0:
        shape = LuminousOpeningShape.ROUND
    elif w < 0 and l < 0 and h < 0:
        shape = LuminousOpeningShape.SPHERE
    elif w < 0 and l > 0 and h < 0:
        shape = LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
    elif w > 0 and l < 0 and h < 0:
        shape = LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
    elif w < 0 and l == 0 and h < 0:
        shape = LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
    else:
        raise InvalidLuminousOpeningException()

    return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f, shape)

def create_luminous_opening(attributes):
    f = 0  # Factor for unit conversion (internally always stored in meters)
    if attributes["luminous_opening_units"] == _UNIT_TYPE_FEET:
            f = 0.3048
    else:
            f = 1

    match attributes["header"].replace(" ", ""):
        case "IESNA:LM-63-2002":
            return create_luminous_opening_for_iesna02(
                attributes["luminous_opening_width"],
                attributes["luminous_opening_length"],
                attributes["luminous_opening_height"],
                f
            )
        case _:
            return create_luminous_opening_for_iesna95(
                attributes["luminous_opening_width"],
                attributes["luminous_opening_length"],
                attributes["luminous_opening_height"],
                f
            )


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
        "header": header,
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

    date = metadata.pop("ISSUEDATE", None) or metadata.pop("DATE", None)
    return Luminaire(
        gamma_angles=v_angles,
        c_planes=h_angles,
        intensity_values=candela_values,
        luminous_opening_geometry=create_luminous_opening(attributes),
        geometry=None,
        photometry=LuminairePhotometricProperties(
            is_absolute=lumens is None,
            luminous_flux=Calculable(None),
            lor=Calculable(None),
            dff=Calculable(None),
            efficacy=Calculable(None)
        ),
        lamps=[Lamps(
            number_of_lamps=attributes["numer_of_lamps"],
            lumens_per_lamp=attributes["lumens_per_lamp"] if attributes["lumens_per_lamp"] >= 0 else None,
            description=metadata.pop("LAMP", None),
            catalog_number=metadata.pop("LAMPCAT", None),
            position=metadata.pop("LAMPPOSITION", None),
            ballast_catalog_number=metadata.pop("BALLASTCAT", None),
            ballast_description=metadata.pop("BALLAST", None),
            wattage=float(input_watts),
            color=metadata.pop("COLORTEMP", None),
            cri=metadata.pop("CRI", None),
        )],
        metadata=PhotometryMetadata(
            catalog_number=metadata.pop("LUMCAT", None),
            luminaire=metadata.pop("LUMINAIRE", None),
            manufacturer=metadata.pop("MANUFAC", None),
            date_and_user=date,
            additional_properties=metadata,
            file_source=source,
            file_units=LengthUnits.FEET if attributes["luminous_opening_units"] == 1 else LengthUnits.METERS
        )
    )


def _write_keywords(f: IO, keywords: Dict[str, str]):
    for k, v in keywords.items():
        if not v: continue
        value = v.replace("\n", "\n[MORE] ")
        f.write(f"[{k}] {value}\r\n")


def _write_luminous_opening_geometry(f, luminaire: Luminaire):
    is_feet = luminaire.metadata.file_units == LengthUnits.FEET
    multiplier = 3.2808 if is_feet else 1

    luminous_opening_geometry = luminaire.luminous_opening_geometry
    match luminous_opening_geometry:
        case LuminousOpeningGeometry(_, _, _, shape=LuminousOpeningShape.POINT):
            f.write("0 0 0 ")
        case LuminousOpeningGeometry(w, l, h, shape=LuminousOpeningShape.RECTANGULAR):
            f.write(f"{w*multiplier:.3f} {l*multiplier:.3f} {h*multiplier:.3f} ")
        case LuminousOpeningGeometry(w, l, h, shape=LuminousOpeningShape.ROUND):
            f.write(f"{-w*multiplier:.3f} {-l*multiplier:.3f} {h*multiplier:.3f} ")
        case LuminousOpeningGeometry(w, l, h, shape=LuminousOpeningShape.SPHERE):
            f.write(f"{-w*multiplier:.3f} {-l*multiplier:.3f} {-h*multiplier:.3f} ")
        case LuminousOpeningGeometry(w, l, h, shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH):
            f.write(f"{w*multiplier:.3f} {-l*multiplier:.3f} {-h*multiplier:.3f} ")
        case LuminousOpeningGeometry(w, l, h, shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH):
            f.write(f"{-w*multiplier:.3f} {l*multiplier:.3f} {-h*multiplier:.3f} ")
        case LuminousOpeningGeometry(w, l, h, shape=_):
            f.write(f"{w*multiplier:.3f} {l*multiplier:.3f} {h*multiplier:.3f} ")

    f.write("\r\n")


def export_to_file(f: IO, luminaire: Luminaire, additional_keywords: Dict[str, str]):
    f.write("IESNA: LM-63-2002\r\n")

    first_lamp_set = luminaire.lamps[0]
    standard_keywords = {
        "TEST": "Unknown",
        "TESTLAB": "Unknown",
        "LUMCAT": luminaire.metadata.catalog_number,
        "LUMINAIRE": luminaire.metadata.luminaire,
        "MANUFAC": luminaire.metadata.manufacturer,
        "ISSUEDATE": luminaire.metadata.date_and_user,
        "LAMP": first_lamp_set.description,
        "LAMPCAT": first_lamp_set.catalog_number,
        "LAMPPOSITION": first_lamp_set.position,
        "COLORTEMP": first_lamp_set.color,
        "CRI": first_lamp_set.cri,
        "BALLASTCAT": first_lamp_set.ballast_catalog_number,
        "BALLAST": luminaire.lamps[0].ballast_description
    }

    _write_keywords(
        f,
        keywords=standard_keywords | luminaire.metadata.additional_properties | additional_keywords
    )

    f.write("TILT=NONE\r\n")

    f.write(f"{luminaire.lamps[0].number_of_lamps} ")

    if luminaire.photometry.is_absolute:
        f.write(f"{_LUMEN_PER_LAMPS_ABSOLUTE} ")
    elif first_lamp_set.lumens_per_lamp:
        f.write(f"{first_lamp_set.lumens_per_lamp} ")
    else:
        f.write(f"{_LUMEN_PER_LAMPS_1000} ")

    f.write(f"{_DEFAULT_MULTIPLIER} ")
    f.write(f"{len(luminaire.gamma_angles)} ")
    f.write(f"{len(luminaire.c_planes)} ")
    f.write(f"{_PHOTOMETRIC_TYPE_C} ")

    if luminaire.metadata.file_units == LengthUnits.FEET:
        f.write(f"{_UNIT_TYPE_FEET} ")
    else:
        f.write(f"{_UNIT_TYPE_METERS} ")

    _write_luminous_opening_geometry(f, luminaire)

    f.write(f"{_DEFAULT_BALLAST_FACTOR} ")
    f.write(f"{_FUTURE_USE} ")
    f.write(f"{first_lamp_set.wattage or 0}\r\n")

    for i, gamma in enumerate(luminaire.gamma_angles):
        f.write(f"{gamma} ")
        if (i+1) % _VALUES_PER_LINE == 0 or (i+1) == len(luminaire.gamma_angles):
            f.write("\r\n")

    for i, c in enumerate(luminaire.c_planes):
        f.write(f"{c} ")
        if (i+1) % _VALUES_PER_LINE == 0 or (i+1) == len(luminaire.c_planes):
            f.write("\r\n")

    i = 0
    for c in luminaire.c_planes:
        for gamma in luminaire.gamma_angles:
            intensity = luminaire.intensity_values[c, gamma]
            if luminaire.photometry.is_absolute:
                intensity *= 1
            elif first_lamp_set.lumens_per_lamp and first_lamp_set.lumens_per_lamp > 0:
                intensity *= first_lamp_set.number_of_lamps * first_lamp_set.lumens_per_lamp / 1000

            f.write(f"{intensity} ")
            if (i+1) % _VALUES_PER_LINE == 0:
                f.write("\r\n")
            i += 1




from typing import IO, Dict

from photometric_viewer.model.luminaire import Luminaire, LuminousOpeningGeometry, LuminousOpeningShape
from photometric_viewer.model.units import LengthUnits

_LUMEN_PER_LAMPS_ABSOLUTE = -1
_LUMEN_PER_LAMPS_1000 = 1000

_DEFAULT_MULTIPLIER = 1.0
_PHOTOMETRIC_TYPE_C = 1
_UNIT_TYPE_FEET = 1
_UNIT_TYPE_METERS = 2
_DEFAULT_BALLAST_FACTOR = 1.0
_FUTURE_USE = 1

_VALUES_PER_LINE = 12


def _write_keywords(f: IO, keywords: Dict[str, str]):
    for k, v in keywords.items():
        if not v:
            continue
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
    f.write("IESNA:LM-63-2002\r\n")

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

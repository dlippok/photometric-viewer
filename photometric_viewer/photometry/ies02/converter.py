from typing import Dict, Tuple

from photometric_viewer.model.luminaire import LuminousOpeningGeometry
from photometric_viewer.model.luminaire import Luminaire, PhotometryMetadata, FileFormat, Lamps, \
    LuminairePhotometricProperties, Calculable, LuminousOpeningShape
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.ies02.model import IesContent
from photometric_viewer.utils.conversion import safe_float


def convert_content(content: IesContent) -> Luminaire:
    metadata = _convert_metadata(content)
    candela_values = _convert_candela_values(content)
    is_absolute = _get_is_absolute(content)

    return Luminaire(
        gamma_angles=content.v_angles,
        c_planes=content.h_angles,
        intensity_values=candela_values,
        geometry=None,
        luminous_opening_geometry=_convert_luminous_opening_geometry(content),
        photometry=LuminairePhotometricProperties(
            is_absolute=is_absolute,
            luminous_flux=Calculable(None),
            lor=Calculable(None),
            dff=Calculable(None),
            efficacy=Calculable(None)
        ),
        lamps=[Lamps(
            number_of_lamps=content.inline_attributes.number_of_lamps,
            lumens_per_lamp=content.inline_attributes.lumens_per_lamp if not is_absolute else None,
            description=metadata.pop("LAMP", None),
            catalog_number=metadata.pop("LAMPCAT", None),
            position=metadata.pop("LAMPPOSITION", None),
            ballast_catalog_number=metadata.pop("BALLASTCAT", None),
            ballast_description=metadata.pop("BALLAST", None),
            wattage=content.lamp_attributes.input_watts,
            color=metadata.pop("COLORTEMP", None),
            cri=metadata.pop("CRI", None),
        )],
        metadata=PhotometryMetadata(
            catalog_number=metadata.pop("LUMCAT", None),
            luminaire=metadata.pop("LUMINAIRE", None),
            manufacturer=metadata.pop("MANUFAC", None),
            date_and_user=metadata.pop("ISSUEDATE", None) or metadata.pop("DATE", None),
            additional_properties=metadata,
            file_source="",
            file_format=FileFormat.IES,
            file_units=_convert_file_units(content)
        )
    )


def _convert_metadata(content: IesContent) -> Dict[str, str]:
    original_metadata = content.metadata
    metadata = {}
    last_key = None

    for t in original_metadata:
        if t.key == "MORE" and last_key is not None:
            metadata[last_key] += "\n" + t.value
        elif t.key in metadata.keys():
            metadata[t.key] += "\n" + t.value
            last_key = t.key
        else:
            metadata[t.key] = t.value
            last_key = t.key
    return metadata


def _convert_candela_values(content: IesContent) -> Dict[Tuple[float, float], float]:
    lumens_per_lamp = content.inline_attributes.lumens_per_lamp or 0
    number_of_lamps = content.inline_attributes.number_of_lamps or 0
    multiplying_factor = content.inline_attributes.multiplying_factor or 0
    ballast_factor = content.lamp_attributes.ballast_factor or 0
    lamp_photometric_factor = content.lamp_attributes.photometric_factor or 0

    lumens = lumens_per_lamp * number_of_lamps
    relative_photometry_divider = lumens / 1000 if lumens_per_lamp >= 0 else 1

    candela_values = {}

    n = 0
    for h_angle in content.h_angles:
        h_angle = safe_float(h_angle)
        for v_angle in content.v_angles:
            v_angle = safe_float(v_angle)
            raw_value = safe_float(content.intensities[n]) if len(content.intensities) >= n else None
            value = raw_value * multiplying_factor * ballast_factor * lamp_photometric_factor
            candela_values[(h_angle, v_angle)] = round(value / relative_photometry_divider, ndigits=2)
            n += 1

    return candela_values


def _convert_file_units(content: IesContent) -> LengthUnits:
    return LengthUnits.FEET if content.inline_attributes.luminous_opening_units == 1 else LengthUnits.METERS


def _convert_luminous_opening_geometry(content: IesContent) -> LuminousOpeningGeometry | None:
    # Factor for unit conversion (internally always stored in meters)
    if _convert_file_units(content) == LengthUnits.FEET:
        f = 0.3048
    else:
        f = 1

    w = content.inline_attributes.luminous_opening_width
    l = content.inline_attributes.luminous_opening_length
    h = content.inline_attributes.luminous_opening_height

    if w is None or l is None or h is None:
        return None

    return _create_luminous_opening(w, l, h, f)


def _create_luminous_opening(
        w: float | None,
        l: float | None,
        h: float | None,
        f: float | None
) -> LuminousOpeningGeometry | None:
    if w is None or l is None or h is None or f is None:
        return None

    if w == 0 and l == 0 and h == 0:
        shape = LuminousOpeningShape.POINT
    elif w > 0 and l > 0 and h == 0:
        shape = LuminousOpeningShape.RECTANGULAR
    elif w > 0 and l > 0 and h > 0:
        shape = LuminousOpeningShape.RECTANGULAR
    elif w < 0 <= h and l < 0:
        shape = LuminousOpeningShape.ROUND
    elif w < 0 and l < 0 and h < 0:
        shape = LuminousOpeningShape.SPHERE
    elif w < 0 < l and h < 0:
        shape = LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
    elif w > 0 > l and h < 0:
        shape = LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
    elif w < 0 and l == 0 and h < 0:
        shape = LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
    else:
        return None

    return LuminousOpeningGeometry(abs(w) * f, abs(l) * f, abs(h) * f, shape)


def _get_is_absolute(content: IesContent) -> bool:
    if content.inline_attributes.lumens_per_lamp is None:
        return False

    if content.inline_attributes.lumens_per_lamp >= 0:
        return False
    return True

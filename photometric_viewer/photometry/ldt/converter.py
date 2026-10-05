from typing import List, Dict, Tuple

from photometric_viewer.model.luminaire import Luminaire, LuminaireGeometry, Shape, LuminousOpeningGeometry, \
    LuminousOpeningShape, \
    LuminairePhotometricProperties, Calculable, Lamps, PhotometryMetadata, FileFormat, Symmetry, LuminaireType
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.iesna_common.model import Attribute
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet
from photometric_viewer.utils.conversion import safe_float, safe_int


def _extract_intensity(intensities: List[float]) -> float | None:
    return intensities.pop(0) if intensities else None


def _is_absolute(content: LdtContent):
    return any(
        safe_int(lamp_set.number_of_lamps.value) is not None
        and safe_int(lamp_set.number_of_lamps.value) < 0
        for lamp_set
        in content.lamp_sets
    )

def _extract_angles(attributes: List[Attribute]) -> List[float ]:
    result = []
    for a in attributes:
        value = safe_float(a.value)
        if value is not None:
            result.append(value)

    return result


def _extract_candela_values(content: LdtContent, c_angles: List[float], gamma_angles: List[float]) -> Dict[Tuple[float, float], float]:
    symmetry = _extract_symmetry(content)
    if content.lamp_sets and _is_absolute(content):
        total_lumens = safe_float(content.lamp_sets[0].total_lumens.value)
        factor = total_lumens / 1000 if total_lumens is not None and total_lumens > 0 else 1.0
    else:
        factor = 1.0

    converted_intensities: List[float] = [
        (safe_float(v.value) or 0) * factor
        for v
        in content.intensities
    ]

    values: Dict[
        Tuple[float | None, float | None],
        float | None
    ] = {}

    if symmetry == Symmetry.NONE:
        for c in c_angles:
            for gamma in gamma_angles:
                values[(c, gamma)] = _extract_intensity(converted_intensities)

    elif symmetry == Symmetry.TO_VERTICAL_AXIS:
        for gamma in gamma_angles:
            value = _extract_intensity(converted_intensities)
            for c in c_angles:
                values[(c, gamma)] = value

    elif symmetry == Symmetry.TO_C0_C180:
        for c in c_angles:
            if c <= 180:
                for gamma in gamma_angles:
                    value = _extract_intensity(converted_intensities)
                    values[(c, gamma)] = value
                    if c != 0:
                        values[(360 - c, gamma)] = value

    elif symmetry == Symmetry.TO_C90_C270:
        angles: List[float | None] = [c for c in c_angles if 270 <= c < 360]
        angles.extend([c for c in c_angles if c <= 90])
        angles.extend([c for c in c_angles if 90 < c < 270])

        for c in angles:
            if 270 <= c < 360:
                for gamma in gamma_angles:
                    value = _extract_intensity(converted_intensities)
                    values[(c, gamma)] = value
                    values[(270 - (c - 270), gamma)] = value
            if c <= 90:
                for gamma in gamma_angles:
                    value = _extract_intensity(converted_intensities)
                    values[(c, gamma)] = value
                    values[(180 - c, gamma)] = value

    elif symmetry == Symmetry.TO_C0_C180_C90_C270:
        for c in c_angles:
            if c <= 90:
                for gamma in gamma_angles:
                    value = _extract_intensity(converted_intensities)
                    values[(c, gamma)] = value
                    values[(180 + c, gamma)] = value
                    if c != 0:
                        values[(360 - c, gamma)] = value
                        values[(180 - c, gamma)] = value

    result = {}
    for k, v in values.items():
        if k[0] is not None and k[1] is not None and v is not None:
            result[k] = v

    return result


def _extract_luminaire_geometry(content: LdtContent) -> LuminaireGeometry | None:
    length = _to_meters(content.length_of_luminaire)
    width = _to_meters(content.width_of_luminaire)
    height = _to_meters(content.height_of_luminaire)

    if length is None or height is None or width is None:
        return None

    return LuminaireGeometry(
        length=length,
        width=width or length,
        height=height,
        shape=Shape.RECTANGULAR if width and width > 0 else Shape.ROUND,
    )


def _to_meters(value: Attribute) -> float | None:
    float_value = safe_float(value.value)
    return float_value / 1000 if float_value is not None else None


def _extract_luminous_opening_geometry(content: LdtContent) -> LuminousOpeningGeometry | None:
    width = _to_meters(content.width_of_luminous_area)
    length = _to_meters(content.length_of_luminous_area)
    height_c0 = _to_meters(content.height_of_luminous_area_c0)
    height_c90 = _to_meters(content.height_of_luminous_area_c90)
    height_c180 = _to_meters(content.height_of_luminous_area_c180)
    height_c270 = _to_meters(content.height_of_luminous_area_c270)

    if width is None or length is None or height_c0 is None or height_c90 is None or height_c180 is None or height_c270 is None:
        return None

    shape = None
    if width == 0.0 and length == 0.0:
        shape = LuminousOpeningShape.POINT
    elif width == 0.0 and length != 0.0:
        shape = LuminousOpeningShape.ROUND
    else:
        shape = LuminousOpeningShape.RECTANGULAR

    return LuminousOpeningGeometry(
        length=length,
        width=width or length,
        height=height_c0,
        height_c90=height_c90,
        height_c180=height_c180,
        height_c270=height_c270,
        shape=shape
    )


def _extract_lamp_set(lamp_set: LampSet) -> Lamps:
    number_of_lamps = safe_int(lamp_set.number_of_lamps.value)
    total_lumens = safe_float(lamp_set.total_lumens.value)

    return Lamps(
        number_of_lamps=abs(number_of_lamps) if number_of_lamps is not None else None,
        lumens_per_lamp=total_lumens / abs(number_of_lamps) if number_of_lamps is not None and number_of_lamps != 0 else None,
        wattage=safe_float(lamp_set.wattage.value),
        color=lamp_set.light_color.value,
        cri=lamp_set.cri.value,
        description=lamp_set.type_of_lamp.value
    )


def _extract_direct_ratios_for_room_indices(content) -> Dict[float, float]:
    result = {}

    for index, value in zip(
        [0.60, 0.80, 1.00, 1.25, 1.50, 2.00, 2.50, 3.00, 4.00, 5.00],
        content.direct_ratios_for_room_indices
    ):
        if safe_float(value.value) is not None:
            result[index] = safe_float(value.value)

    return result


def _extract_light_source_type(content: LdtContent):
    match content.type_indicator.value:
        case "1":
            return LuminaireType.POINT_SOURCE_WITH_VERTICAL_SYMMETRY
        case "2":
            return LuminaireType.LINEAR
        case _:
            return LuminaireType.POINT_SOURCE_WITH_OTHER_SYMMETRY


def _extract_lor(content: LdtContent) -> Calculable:
    if content.lor_percent.value is None:
        return Calculable(None)

    lor_percent = safe_float(content.lor_percent.value)
    if not lor_percent or lor_percent < 0 or lor_percent > 100:
        return Calculable(None)

    return Calculable(lor_percent / 100)


def _extract_luminous_flux(content: LdtContent) -> Calculable:
    if not _is_absolute(content):
        return Calculable(None)

    if not content.lamp_sets:
        return Calculable(None)

    total_lumens = safe_float(content.lamp_sets[0].total_lumens.value)
    if content.lamp_sets and total_lumens is not None:
        return Calculable(total_lumens)

    return Calculable(None)


def _extract_efficacy(content: LdtContent) -> Calculable:
    if not _is_absolute(content):
        return Calculable(None)

    if not content.lamp_sets:
        return Calculable(None)

    total_lumens = safe_float(content.lamp_sets[0].total_lumens.value)
    wattage = safe_float(content.lamp_sets[0].wattage.value)

    if total_lumens and wattage and wattage > 0:
        return Calculable(total_lumens / wattage)

    return Calculable(None)


def _extract_symmetry(content: LdtContent) -> Symmetry:
    match content.symmetry_indicator.value:
        case "1":
            return Symmetry.TO_VERTICAL_AXIS
        case "2":
            return Symmetry.TO_C0_C180
        case "3":
            return Symmetry.TO_C90_C270
        case "4":
            return Symmetry.TO_C0_C180_C90_C270
        case _:
            return Symmetry.NONE



def convert_content(content: LdtContent) -> Luminaire:
    c_angles = _extract_angles(content.c_angles)
    gamma_angles = _extract_angles(content.gamma_angles)

    return Luminaire(
        gamma_angles=gamma_angles,
        c_planes=c_angles,
        intensity_values=_extract_candela_values(content, c_angles, gamma_angles),
        geometry=_extract_luminaire_geometry(content),
        luminous_opening_geometry=_extract_luminous_opening_geometry(content),
        photometry=LuminairePhotometricProperties(
            is_absolute=_is_absolute(content),
            luminous_flux=_extract_luminous_flux(content),
            lor=Calculable(content.lor_percent).from_percent(),
            dff=Calculable(content.dff_percent).from_percent(),
            efficacy=_extract_efficacy(content)
        ),
        lamps=[_extract_lamp_set(lamp_set) for lamp_set in content.lamp_sets],
        metadata=PhotometryMetadata(
            catalog_number=content.luminaire_number.value,
            luminaire=content.luminaire_name.value,
            manufacturer=content.header.value,
            file_format=FileFormat.EULUMDAT,
            file_units=LengthUnits.MILLIMETERS,
            luminaire_type=_extract_light_source_type(content),
            measurement=content.measurement_report.value,
            date_and_user=content.date_and_user.value,
            conversion_factor=safe_float(content.conversion_factor.value),
            filename=content.file_name.value,
            additional_properties={},
            symmetry=_extract_symmetry(content),
            direct_ratios_for_room_indices=_extract_direct_ratios_for_room_indices(content)
        )
    )
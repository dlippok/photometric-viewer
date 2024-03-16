from typing import List

from photometric_viewer.model.luminaire import Luminaire, LuminaireGeometry, Shape, LuminousOpeningGeometry, \
    LuminousOpeningShape, \
    LuminairePhotometricProperties, Calculable, Lamps, PhotometryMetadata, FileFormat, Symmetry, LuminaireType
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet


def _extract_intensity(intensities: List[float]) -> float | None:
    return intensities.pop(0) if intensities else None


def _is_absolute(content: LdtContent):
    return any(
        lamp_set.number_of_lamps is not None
        and lamp_set.number_of_lamps < 0
        for lamp_set
        in content.lamp_sets
    )


def _extract_candela_values(content: LdtContent) -> dict[tuple[float, float], float]:
    symmetry = _extract_symmetry(content)

    c_angles = [c for c in content.c_angles if c is not None]
    gamma_angles = [g for g in content.gamma_angles if g is not None]

    if content.lamp_sets and _is_absolute(content):
        factor = content.lamp_sets[0].total_lumens / 1000
    else:
        factor = 1
    converted_intensities = [(v or 0) * factor for v in content.intensities]

    values = {}

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
        angles = [c for c in c_angles if 270 <= c < 360]
        angles += [c for c in c_angles if c <= 90]
        angles += [c for c in c_angles if 90 < c < 270]

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

    return {k: v for k, v in values.items() if v is not None}


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


def _to_meters(value: float | None) -> float | None:
    return value / 1000 if value is not None else None


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
    match content.length_of_luminous_area, content.width_of_luminous_area:
        case 0, 0:
            shape = LuminousOpeningShape.POINT
        case l, 0:
            shape = LuminousOpeningShape.ROUND
        case l, w:
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
    return Lamps(
        number_of_lamps=abs(lamp_set.number_of_lamps) if lamp_set.number_of_lamps else None,
        lumens_per_lamp=lamp_set.total_lumens / abs(lamp_set.number_of_lamps) if lamp_set.total_lumens else None,
        wattage=lamp_set.wattage,
        color=lamp_set.light_color,
        cri=lamp_set.cri,
        description=lamp_set.type_of_lamp
    )


def _extract_direct_ratios_for_room_indices(content):
    return {
        index: value for index, value in zip(
            [0.60, 0.80, 1.00, 1.25, 1.50, 2.00, 2.50, 3.00, 4.00, 5.00],
            content.direct_ratios_for_room_indices
        )
        if value is not None
    }


def _extract_light_source_type(content: LdtContent):
    match content.type_indicator:
        case 1:
            return LuminaireType.POINT_SOURCE_WITH_VERTICAL_SYMMETRY
        case 2:
            return LuminaireType.LINEAR
        case 3:
            return LuminaireType.POINT_SOURCE_WITH_OTHER_SYMMETRY


def _extract_lor(content: LdtContent) -> Calculable:
    if content.lor_percent is None:
        return Calculable(None)

    return Calculable(content.lor_percent / 100)


def _extract_luminous_flux(content: LdtContent) -> Calculable:
    if not _is_absolute(content):
        return Calculable(None)

    if content.lamp_sets and content.lamp_sets[0].total_lumens:
        return Calculable(content.lamp_sets[0].total_lumens)

    return Calculable(None)


def _extract_efficacy(content: LdtContent) -> Calculable:
    if not _is_absolute(content):
        return Calculable(None)

    if content.lamp_sets and content.lamp_sets[0].total_lumens and content.lamp_sets[0].wattage:
        return Calculable(content.lamp_sets[0].total_lumens / content.lamp_sets[0].wattage)

    return Calculable(None)


def _extract_symmetry(content: LdtContent) -> Symmetry:
    match content.symmetry_indicator:
        case 1:
            return Symmetry.TO_VERTICAL_AXIS
        case 2:
            return Symmetry.TO_C0_C180
        case 3:
            return Symmetry.TO_C90_C270
        case 4:
            return Symmetry.TO_C0_C180_C90_C270
        case _:
            return Symmetry.NONE


def convert_content(content: LdtContent) -> Luminaire:
    return Luminaire(
        gamma_angles=content.gamma_angles,
        c_planes=content.c_angles,
        intensity_values=_extract_candela_values(content),
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
            catalog_number=content.luminaire_number,
            luminaire=content.luminaire_name,
            manufacturer=content.header,
            file_format=FileFormat.LDT,
            file_units=LengthUnits.MILLIMETERS,
            luminaire_type=_extract_light_source_type(content),
            measurement=content.measurement_report,
            date_and_user=content.date_and_user,
            conversion_factor=content.conversion_factor,
            filename=content.file_name,
            file_source=None,
            additional_properties={},
            symmetry=_extract_symmetry(content),
            direct_ratios_for_room_indices=_extract_direct_ratios_for_room_indices(content)
        )
    )
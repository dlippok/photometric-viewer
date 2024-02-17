from enum import Enum
from typing import IO, List, Callable

from datetime import datetime
from photometric_viewer.model.luminaire import Luminaire, LuminousOpeningGeometry, Shape, Lamps, \
    PhotometryMetadata, LuminaireGeometry, LuminaireType, LuminousOpeningShape, Symmetry, \
    LuminairePhotometricProperties, Calculable, FileFormat
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.utils.conversion import safe_int, safe_float


def _create_luminous_opening(length, width, height_c0, height_c90, height_c180, height_c270) -> LuminousOpeningGeometry:
    shape = None
    match length, width:
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


def _create_luminaire_geometry(length, width, height) -> LuminaireGeometry:
    return LuminaireGeometry(
        length=length,
        width=width or length,
        height=height,
        shape=Shape.RECTANGULAR if width > 0 else Shape.ROUND,
    )


def _get_source_type(light_source_type: int):
    match light_source_type:
        case 1: return LuminaireType.POINT_SOURCE_WITH_VERTICAL_SYMMETRY
        case 2: return LuminaireType.LINEAR
        case 3: return LuminaireType.POINT_SOURCE_WITH_OTHER_SYMMETRY


def import_from_file(f: IO):
    manufacturer = f.readline().strip()
    light_source_type = safe_int(f.readline().strip())
    try:
        symmetry = Symmetry(safe_int(f.readline().strip()))
    except ValueError:
        symmetry = Symmetry.NONE

    n_c_angles = safe_int(f.readline().strip())
    c_angle_interval = safe_float(f.readline().strip())
    values_per_c_plane = safe_int(f.readline().strip())
    values_angle_interval = safe_float(f.readline().strip())
    measurement = f.readline().strip()
    luminaire_name = f.readline().strip()
    luminaire_catalog_number = f.readline().strip()
    filename = f.readline().strip()
    date_and_user = f.readline().strip()
    luminaire_length = safe_float(f.readline().strip()) / 1000
    luminaire_width = safe_float(f.readline().strip()) / 1000
    luminaire_height = safe_float(f.readline().strip()) / 1000
    opening_length = safe_float(f.readline().strip()) / 1000
    opening_width = safe_float(f.readline().strip()) / 1000
    opening_height_c0 = safe_float(f.readline().strip()) / 1000
    opening_height_c90 = safe_float(f.readline().strip()) / 1000
    opening_height_c180 = safe_float(f.readline().strip()) / 1000
    opening_height_c270 = safe_float(f.readline().strip()) / 1000
    dff = safe_float(f.readline().strip()) / 100
    lorl = safe_float(f.readline().strip()) / 100
    conversion_factor = safe_float(f.readline().strip())
    tilt = safe_float(f.readline().strip())
    no_lamp_sets = safe_int(f.readline().strip())

    lamp_sets = []
    is_absolute = False

    for sets in range(no_lamp_sets):
        no_lamps = safe_int(f.readline().strip())
        lamp_sets.append({
                "number_of_lamps": abs(no_lamps),
                "type": f.readline().strip(),
                "luminous_flux": safe_float(f.readline().strip()),
                "color": f.readline().strip(),
                "cri": f.readline().strip(),
                "wattage": safe_float(f.readline().strip())
            }
        )
        is_absolute = no_lamps < 0

    ratios_for_room_indexes = [
        safe_float(f.readline().strip())
        for _ in range(10)
    ]

    c_angles = [
        safe_float(f.readline().strip())
        for _ in range(n_c_angles)
    ][:1000]

    gamma_angles = [
        safe_float(f.readline().strip())
        for _ in range(values_per_c_plane)
    ][:1000]

    values = {}

    if symmetry == Symmetry.NONE:
        for c in c_angles:
            for gamma in gamma_angles:
                raw_value = safe_float(f.readline().strip())
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_VERTICAL_AXIS:
        for gamma in gamma_angles:
            raw_value = safe_float(f.readline().strip())
            for c in c_angles:
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_C0_C180:
        for c in c_angles:
            if c <= 180:
                for gamma in gamma_angles:
                    raw_value = safe_float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    if c != 0:
                        values[(360-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_C90_C270:
        for c in c_angles:
            if 90 <= c <= 180:
                for gamma in gamma_angles:
                    raw_value = safe_float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(90 - (c - 90), gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
            if 180 < c <= 270:
                for gamma in gamma_angles:
                    raw_value = safe_float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(360 - (c - 180), gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_C0_C180_C90_C270:
        for c in c_angles:
            if c <= 90:
                for gamma in gamma_angles:
                    raw_value = safe_float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(180+c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    if c != 0:
                        values[(360-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                        values[(180-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value

    f.seek(0)
    source = f.read()

    luminaire_flux = lamp_sets[0]["luminous_flux"] if is_absolute else None
    luminaire_efficacy = lamp_sets[0]["luminous_flux"] / lamp_sets[0]["wattage"] if is_absolute else None

    return Luminaire(
        gamma_angles=gamma_angles,
        c_planes=c_angles,
        intensity_values=values,
        luminous_opening_geometry=_create_luminous_opening(
            opening_length,
            opening_width,
            opening_height_c0,
            opening_height_c90,
            opening_height_c180,
            opening_height_c270
        ),
        photometry=LuminairePhotometricProperties(
            is_absolute=is_absolute,
            luminous_flux=Calculable(luminaire_flux),
            efficacy=Calculable(luminaire_efficacy),
            lor=Calculable(lorl),
            dff=Calculable(dff)
        ),
        geometry=_create_luminaire_geometry(luminaire_length, luminaire_width, luminaire_height),
        lamps=[Lamps(
            number_of_lamps=lamps["number_of_lamps"],
            lumens_per_lamp=lamps["luminous_flux"] / max(lamps["number_of_lamps"], 1),
            wattage=lamps["wattage"],
            color=lamps["color"],
            cri=lamps["cri"],
            description=lamps["type"],
            catalog_number=None,
            position=None,
            ballast_catalog_number=None,
            ballast_description=None
        ) for lamps in lamp_sets],
        metadata=PhotometryMetadata(
            catalog_number=luminaire_catalog_number,
            luminaire=luminaire_name,
            manufacturer=manufacturer,
            file_source=source,
            file_format=FileFormat.LDT,
            file_units=LengthUnits.MILLIMETERS,
            luminaire_type=_get_source_type(light_source_type),
            measurement=measurement,
            date_and_user=date_and_user,
            conversion_factor=conversion_factor,
            filename=filename,
            additional_properties={},
            symmetry=Symmetry(symmetry),
            direct_ratios_for_room_indices=ratios_for_room_indexes
        )
    )


def _write_line(f: IO, value: str, max_len: int = 0):
    if not value:
        f.write("\r\n")
    elif 0 < max_len < len(value):
        normalized_value = value.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        f.write(normalized_value[0:max_len] + "\r\n")
    else:
        f.write(value + "\r\n")


def _write_enum(f: IO, value: Enum | None, default: str = "0"):
    if value:
        f.write(str(value.value) + "\r\n")
    else:
        f.write(default + "\r\n")


def _write_size(f: IO, value: float | int | None, default: float | int = 0):
    if value is not None:
        f.write(str(value * 1000) + "\r\n")
    else:
        f.write(str(default * 1000) + "\r\n")


def _write_number(f: IO, value: float | int | None, default: float | int = 0, ndigits: int = 3):
    if value is not None:
        f.write(str(round(value, ndigits=ndigits)) + "\r\n")
    else:
        f.write(str(default) + "\r\n")


def _write_numbers(f: IO, values: List[float] | List[int] | None, default: List[float] | List[int]):
    if values is not None:
        for value in values:
            f.write(str(value) + "\r\n")
    else:
        for value in default:
            f.write(str(value) + "\r\n")

def _write_gamma_values(f: IO, luminaire: Luminaire, c_plane_predicate: Callable[[float], bool]):
    for c_plane in luminaire.c_planes:
        if not c_plane_predicate(c_plane):
            continue
        for gamma_angle in luminaire.gamma_angles:
            intensity = luminaire.intensity_values[(c_plane, gamma_angle)]
            if luminaire.photometry.is_absolute:
                lamp = luminaire.lamps[0]
                if lamp.lumens_per_lamp:
                    _write_number(f, intensity / (lamp.lumens_per_lamp * lamp.number_of_lamps) * 1000)
                else:
                    _write_number(f, intensity)
            else:
                _write_number(f, intensity)


def export_to_file(f: IO, luminaire: Luminaire):
    _write_line(f, luminaire.metadata.manufacturer, max_len=78)
    _write_enum(f, luminaire.metadata.luminaire_type, "0")
    _write_enum(f, luminaire.metadata.symmetry, "0")
    _write_line(f, str(len(luminaire.c_planes)))
    _write_line(f, "0")
    _write_line(f, str(len(luminaire.gamma_angles)))
    _write_line(f, "0")
    _write_line(f, luminaire.metadata.measurement, max_len=78)
    _write_line(f, luminaire.metadata.luminaire, max_len=78)
    _write_line(f, luminaire.metadata.catalog_number, max_len=78)
    _write_line(f, luminaire.metadata.filename)
    date_and_user = luminaire.metadata.date_and_user or datetime.today().strftime("%Y-%m-%d") + " exported by Photometry"
    _write_line(f, date_and_user, max_len=78)

    if luminaire.geometry:
        _write_size(f, luminaire.geometry.length)
        if luminaire.geometry.shape == Shape.RECTANGULAR:
            _write_size(f, luminaire.geometry.width)
        else:
            _write_size(f, 0)
        _write_size(f, luminaire.geometry.height)
    else:
        _write_line(f, str(luminaire.luminous_opening_geometry.length * 1000), max_len=4)
        if luminaire.luminous_opening_geometry.shape == LuminousOpeningShape.RECTANGULAR:
            _write_size(f, luminaire.luminous_opening_geometry.width)
        else:
            _write_size(f, 0)
        _write_size(f, luminaire.luminous_opening_geometry.height)

    opening = luminaire.luminous_opening_geometry
    _write_size(f, opening.length)

    match luminaire.luminous_opening_geometry.shape:
        case LuminousOpeningShape.RECTANGULAR:
            _write_size(f, opening.width)
        case LuminousOpeningShape.ELLIPSE_ALONG_LENGTH:
            _write_size(f, opening.width)
        case LuminousOpeningShape.ELLIPSE_ALONG_WIDTH:
            _write_size(f, opening.width)
        case LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH:
            _write_size(f, opening.width)
        case LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH:
            _write_size(f, opening.width)
        case _:
            _write_size(f, 0)

    _write_size(f, opening.height)
    _write_size(f, opening.height_c90, default=opening.height)
    _write_size(f, opening.height_c180, default=opening.height)
    _write_size(f, opening.height_c270, default=opening.height)

    dff = luminaire.photometry.dff.value or 1
    _write_number(f, dff * 100)

    lor = luminaire.photometry.lor.value or 1
    _write_number(f, lor * 100)
    _write_number(f, luminaire.metadata.conversion_factor, 1)
    _write_number(f, 0)
    _write_number(f, len(luminaire.lamps))
    for lamp in luminaire.lamps:
        if luminaire.photometry.is_absolute:
            _write_number(f, -lamp.number_of_lamps)
        else:
            _write_number(f, lamp.number_of_lamps)
        _write_line(f, lamp.description)
        if lamp.lumens_per_lamp:
            _write_number(f, lamp.lumens_per_lamp * lamp.number_of_lamps)
        else:
            _write_number(f, 1000)
        _write_line(f, lamp.color)
        _write_line(f, lamp.cri)
        _write_number(f, lamp.wattage)

    ratios_for_room_indices = [0 for _ in range(10)]
    if luminaire.metadata.direct_ratios_for_room_indices:
        for i, ratio in enumerate(luminaire.metadata.direct_ratios_for_room_indices):
            if i < len(ratios_for_room_indices):
                ratios_for_room_indices[i] = ratio

    for ratio in ratios_for_room_indices:
        _write_number(f, ratio, ndigits=5)

    for c_plane in luminaire.c_planes:
        _write_number(f, c_plane)

    for gamma_angle in luminaire.gamma_angles:
        _write_number(f, gamma_angle)

    match luminaire.metadata.symmetry:
        case Symmetry.NONE:
            _write_gamma_values(f, luminaire, lambda _: True)
        case Symmetry.TO_VERTICAL_AXIS:
            _write_gamma_values(f, luminaire, lambda c: c == 0)
        case Symmetry.TO_C0_C180:
            _write_gamma_values(f, luminaire, lambda c: c <= 180)
        case Symmetry.TO_C90_C270:
            _write_gamma_values(f, luminaire, lambda c: 90 <= c <= 270)
        case Symmetry.TO_C0_C180_C90_C270:
            _write_gamma_values(f, luminaire, lambda c: c <= 90)
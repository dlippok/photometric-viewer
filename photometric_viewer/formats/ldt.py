from enum import Enum
from typing import IO, List, Callable

from datetime import datetime
from photometric_viewer.model.photometry import Photometry, LuminousOpeningGeometry, Shape, Lamps, \
    PhotometryMetadata, LuminaireGeometry, LuminaireType, LuminousOpeningShape, Symmetry
from photometric_viewer.model.units import LengthUnits


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
    light_source_type = int(f.readline().strip())
    symmetry = Symmetry(int(f.readline().strip()))
    n_c_angles = int(f.readline().strip())
    c_angle_interval = float(f.readline().strip())
    values_per_c_plane = int(f.readline().strip())
    values_angle_interval = float(f.readline().strip())
    measurement = f.readline().strip()
    luminaire_name = f.readline().strip()
    luminaire_catalog_number = f.readline().strip()
    filename = f.readline().strip()
    date_and_user = f.readline().strip()
    luminaire_length = float(f.readline().strip()) / 1000
    luminaire_width = float(f.readline().strip()) / 1000
    luminaire_height = float(f.readline().strip()) / 1000
    opening_length = float(f.readline().strip()) / 1000
    opening_width = float(f.readline().strip()) / 1000
    opening_height_c0 = float(f.readline().strip()) / 1000
    opening_height_c90 = float(f.readline().strip()) / 1000
    opening_height_c180 = float(f.readline().strip()) / 1000
    opening_height_c270 = float(f.readline().strip()) / 1000
    dff = float(f.readline().strip())
    lorl = float(f.readline().strip())
    conversion_factor = float(f.readline().strip())
    tilt = float(f.readline().strip())
    no_lamp_sets = int(f.readline().strip())

    lamp_sets = []
    for sets in range(no_lamp_sets):
        no_lamps = int(f.readline().strip())
        lamp_sets.append({
                "number_of_lamps": abs(no_lamps),
                "type": f.readline().strip(),
                "luminous_flux": float(f.readline().strip()),
                "color": f.readline().strip(),
                "cri": f.readline().strip(),
                "wattage": float(f.readline().strip())
            }
        )
        is_absolute = no_lamps < 0

    ratios_for_room_indexes = [
        float(f.readline().strip())
        for _ in range(10)
    ]

    c_angles = [
        float(f.readline().strip())
        for _ in range(n_c_angles)
    ]

    gamma_angles = [
        float(f.readline().strip())
        for _ in range(values_per_c_plane)
    ]

    values = {}

    if symmetry == Symmetry.NONE:
        for c in c_angles:
            for gamma in gamma_angles:
                raw_value = float(f.readline().strip())
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_VERTICAL_AXIS:
        for gamma in gamma_angles:
            raw_value = float(f.readline().strip())
            for c in c_angles:
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_C0_C180:
        for c in c_angles:
            if c <= 180:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    if c != 0:
                        values[(360-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_C90_C270:
        for c in c_angles:
            if 90 <= c <= 180:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(90 - (c - 90), gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
            if 180 < c <= 270:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(360 - (c - 180), gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == Symmetry.TO_C0_C180_C90_C270:
        for c in c_angles:
            if c <= 90:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(180+c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    if c != 0:
                        values[(360-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                        values[(180-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value

    f.seek(0)
    source = f.read()

    return Photometry(
        is_absolute=is_absolute,
        gamma_angles=gamma_angles,
        c_planes=c_angles,
        intensity_values=values,
        dff=dff,
        lorl=lorl,
        luminous_opening_geometry=_create_luminous_opening(
            opening_length,
            opening_width,
            opening_height_c0,
            opening_height_c90,
            opening_height_c180,
            opening_height_c270
        ),
        luminaire_geometry=_create_luminaire_geometry(luminaire_length, luminaire_width, luminaire_height),
        lamps=[Lamps(
            number_of_lamps=lamps["number_of_lamps"],
            lumens_per_lamp=lamps["luminous_flux"] / lamps["number_of_lamps"],
            is_absolute=is_absolute,
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

def _write_gamma_values(f: IO, photometry: Photometry, c_plane_predicate: Callable[[float], bool]):
    for c_plane in photometry.c_planes:
        if not c_plane_predicate(c_plane):
            continue
        for gamma_angle in photometry.gamma_angles:
            intensity = photometry.intensity_values[(c_plane, gamma_angle)]
            if photometry.is_absolute:
                lamp = photometry.lamps[0]
                if lamp.lumens_per_lamp:
                    _write_number(f, intensity / (lamp.lumens_per_lamp * lamp.number_of_lamps) * 1000)
                else:
                    _write_number(f, intensity)
            else:
                _write_number(f, intensity)


def export_to_file(f: IO, photometry: Photometry):
    _write_line(f, photometry.metadata.manufacturer, max_len=78)
    _write_enum(f, photometry.metadata.luminaire_type, "0")
    _write_enum(f, photometry.metadata.symmetry, "0")
    _write_line(f, str(len(photometry.c_planes)))
    _write_line(f, "0")
    _write_line(f, str(len(photometry.gamma_angles)))
    _write_line(f, "0")
    _write_line(f, photometry.metadata.measurement, max_len=78)
    _write_line(f, photometry.metadata.luminaire, max_len=78)
    _write_line(f, photometry.metadata.catalog_number, max_len=78)
    _write_line(f, photometry.metadata.filename)
    date_and_user = photometry.metadata.date_and_user or datetime.today().strftime("%Y-%m-%d") + " exported by Photometric Viewer"
    _write_line(f, date_and_user, max_len=78)

    if photometry.luminaire_geometry:
        _write_size(f, photometry.luminaire_geometry.length)
        if photometry.luminaire_geometry.shape == Shape.RECTANGULAR:
            _write_size(f, photometry.luminaire_geometry.width)
        else:
            _write_size(f, 0)
        _write_size(f, photometry.luminaire_geometry.height)
    else:
        _write_line(f, str(photometry.luminous_opening_geometry.length * 1000), max_len=4)
        if photometry.luminous_opening_geometry.shape == LuminousOpeningShape.RECTANGULAR:
            _write_size(f, photometry.luminous_opening_geometry.width)
        else:
            _write_size(f, 0)
        _write_size(f, photometry.luminous_opening_geometry.height)

    opening = photometry.luminous_opening_geometry
    _write_size(f, opening.length)

    match photometry.luminous_opening_geometry.shape:
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

    _write_number(f, photometry.dff, 100)
    _write_number(f, photometry.lorl, 100)
    _write_number(f, photometry.metadata.conversion_factor, 1)
    _write_number(f, 0)
    _write_number(f, len(photometry.lamps))
    for lamp in photometry.lamps:
        if photometry.is_absolute:
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
    if photometry.metadata.direct_ratios_for_room_indices:
        for i, ratio in enumerate(photometry.metadata.direct_ratios_for_room_indices):
            if i < len(ratios_for_room_indices):
                ratios_for_room_indices[i] = ratio

    for ratio in ratios_for_room_indices:
        _write_number(f, ratio, ndigits=5)

    for c_plane in photometry.c_planes:
        _write_number(f, c_plane)

    for gamma_angle in photometry.gamma_angles:
        _write_number(f, gamma_angle)

    match photometry.metadata.symmetry:
        case Symmetry.NONE:
            _write_gamma_values(f, photometry, lambda _: True)
        case Symmetry.TO_VERTICAL_AXIS:
            _write_gamma_values(f, photometry, lambda c: c == 0)
        case Symmetry.TO_C0_C180:
            _write_gamma_values(f, photometry, lambda c: c <= 180)
        case Symmetry.TO_C90_C270:
            _write_gamma_values(f, photometry, lambda c: 90 <= c <= 270)
        case Symmetry.TO_C0_C180_C90_C270:
            _write_gamma_values(f, photometry, lambda c: c <= 90)
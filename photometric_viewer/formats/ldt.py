from datetime import datetime
from enum import Enum
from typing import IO, List, Callable

from photometric_viewer.model.luminaire import Luminaire, Shape, LuminousOpeningShape, Symmetry


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
        ratios_for_room_indices = [
            luminaire.metadata.direct_ratios_for_room_indices.get(index, "")
            for index in [0.6, 0.8, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5]
        ]

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
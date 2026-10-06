from typing import IO, Any, Tuple, List

from photometric_viewer.photometry.common import Attribute
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet
from photometric_viewer.utils.ioutil import read_till_end
from photometric_viewer.utils.conversion import safe_int


def _read_attr(f: IO, line_number: int) -> Tuple[Attribute, int]:
    raw = f.readline()
    if raw == "":
        return Attribute(None, line_number), line_number
    value = raw.strip()
    return Attribute(value, line_number), line_number + 1


def extract_lamp_set(f: IO, line_number: int) -> tuple[LampSet, int]:
    number_of_lamps, line_number = _read_attr(f, line_number)
    type_of_lamp, line_number = _read_attr(f, line_number)
    total_lumens, line_number = _read_attr(f, line_number)
    light_color, line_number = _read_attr(f, line_number)
    cri, line_number = _read_attr(f, line_number)
    wattage, line_number = _read_attr(f, line_number)

    return LampSet(
        number_of_lamps=number_of_lamps,
        type_of_lamp=type_of_lamp,
        total_lumens=total_lumens,
        light_color=light_color,
        cri=cri,
        wattage=wattage,
    ), line_number


def extract_content(f: IO) -> LdtContent:
    line_number = 1

    header, line_number = _read_attr(f, line_number)
    type_indicator, line_number = _read_attr(f, line_number)
    symmetry_indicator, line_number = _read_attr(f, line_number)
    number_of_c_planes, line_number = _read_attr(f, line_number)
    distance_between_c_planes, line_number = _read_attr(f, line_number)
    number_of_intensities, line_number = _read_attr(f, line_number)
    distance_between_intensities, line_number = _read_attr(f, line_number)
    measurement_report, line_number = _read_attr(f, line_number)
    luminaire_name, line_number = _read_attr(f, line_number)
    luminaire_number, line_number = _read_attr(f, line_number)
    file_name, line_number = _read_attr(f, line_number)
    date_and_user, line_number = _read_attr(f, line_number)
    length_of_luminaire, line_number = _read_attr(f, line_number)
    width_of_luminaire, line_number = _read_attr(f, line_number)
    height_of_luminaire, line_number = _read_attr(f, line_number)
    length_of_luminous_area, line_number = _read_attr(f, line_number)
    width_of_luminous_area, line_number = _read_attr(f, line_number)
    height_of_luminous_area_c0, line_number = _read_attr(f, line_number)
    height_of_luminous_area_c90, line_number = _read_attr(f, line_number)
    height_of_luminous_area_c180, line_number = _read_attr(f, line_number)
    height_of_luminous_area_c270, line_number = _read_attr(f, line_number)
    dff_percent, line_number = _read_attr(f, line_number)
    lor_percent, line_number = _read_attr(f, line_number)
    conversion_factor, line_number = _read_attr(f, line_number)
    tilt, line_number = _read_attr(f, line_number)
    number_of_lamp_sets, line_number = _read_attr(f, line_number)

    lamp_sets: List[LampSet] = []
    n_sets = safe_int(number_of_lamp_sets.value)  or 0
    if number_of_lamp_sets.value is not None:
        for _ in range(n_sets):
            lamp_set, line_number = extract_lamp_set(f, line_number)
            lamp_sets.append(lamp_set)

    direct_ratios_for_room_indices: List[Attribute] = []
    for _ in range(10):
        ratio, line_number = _read_attr(f, line_number)
        direct_ratios_for_room_indices.append(ratio)

    c_angles: List[Attribute] = []
    n_c_planes = safe_int(number_of_c_planes.value) or 0
    for _ in range(n_c_planes):
        angle, line_number = _read_attr(f, line_number)
        c_angles.append(angle)

    gamma_angles: List[Attribute] = []
    n_gamma_angles = safe_int(number_of_intensities.value) or 0

    for _ in range(n_gamma_angles):
        gamma_angle, line_number = _read_attr(f, line_number)
        gamma_angles.append(gamma_angle)

    intensities: List[Attribute] = [
        Attribute(value, line + line_number - 1)
        for value, line in read_till_end(f)
    ]

    return LdtContent(
        header=header,
        type_indicator=type_indicator,
        symmetry_indicator=symmetry_indicator,
        number_of_c_planes=number_of_c_planes,
        distance_between_c_planes=distance_between_c_planes,
        number_of_intensities=number_of_intensities,
        distance_between_intensities=distance_between_intensities,
        measurement_report=measurement_report,
        luminaire_name=luminaire_name,
        luminaire_number=luminaire_number,
        file_name=file_name,
        date_and_user=date_and_user,
        length_of_luminaire=length_of_luminaire,
        width_of_luminaire=width_of_luminaire,
        height_of_luminaire=height_of_luminaire,
        length_of_luminous_area=length_of_luminous_area,
        width_of_luminous_area=width_of_luminous_area,
        height_of_luminous_area_c0=height_of_luminous_area_c0,
        height_of_luminous_area_c90=height_of_luminous_area_c90,
        height_of_luminous_area_c180=height_of_luminous_area_c180,
        height_of_luminous_area_c270=height_of_luminous_area_c270,
        dff_percent=dff_percent,
        lor_percent=lor_percent,
        conversion_factor=conversion_factor,
        tilt=tilt,
        number_of_lamp_sets=number_of_lamp_sets,
        lamp_sets=lamp_sets,
        direct_ratios_for_room_indices=direct_ratios_for_room_indices,
        c_angles=c_angles,
        gamma_angles=gamma_angles,
        intensities=intensities
    )

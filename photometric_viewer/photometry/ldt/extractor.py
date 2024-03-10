from typing import IO

from photometric_viewer.photometry.ldt.model import LdtContent, LampSet
from photometric_viewer.utils.conversion import safe_int, safe_float
from photometric_viewer.utils.ioutil import read_line


def extract_lamp_set(f) -> LampSet:
    return LampSet(
        number_of_lamps=safe_int(f.readline().strip()),
        type_of_lamp=f.readline().strip(),
        total_lumens=safe_float(f.readline().strip()),
        light_color=f.readline().strip(),
        cri=safe_int(f.readline().strip()),
        wattage=safe_float(f.readline().strip())
    )


def extract_intensities(
        f: IO,
        symmetry: int,
        num_c: int,
        num_gamma: int
) -> list[float]:
    match symmetry:
        case 0:
            mc1 = 1
            mc2 = num_c
        case 1:
            mc1 = 1
            mc2 = 1
        case 2:
            mc1 = 1
            mc2 = (num_c // 2) + 1
        case 3:
            mc1 = (3 * num_c // 4) + 1
            mc2 = num_c // 2
        case 4:
            mc1 = 1
            mc2 = (num_c // 4) + 1
        case _:
            return []
    n_intensities = (mc2-mc1+1) * num_gamma
    return [safe_float(f.readline().strip()) for _ in range(n_intensities)]


def extract_content(f: IO) -> LdtContent:
    header = read_line(f)
    type_indicator = safe_int(f.readline().strip())
    symmetry_indicator = safe_int(f.readline().strip())
    number_of_c_planes = safe_int(f.readline().strip())
    distance_between_c_planes = safe_float(f.readline().strip())
    number_of_intensities = safe_int(f.readline().strip())
    distance_between_intensities = safe_float(f.readline().strip())
    measurement_report = read_line(f)
    luminaire_name = read_line(f)
    luminaire_number = read_line(f)
    file_name = read_line(f)
    date_and_user = read_line(f)
    length_of_luminaire = safe_float(f.readline().strip())
    width_of_luminaire = safe_float(f.readline().strip())
    height_of_luminaire = safe_float(f.readline().strip())
    length_of_luminous_area = safe_float(f.readline().strip())
    width_of_luminous_area = safe_float(f.readline().strip())
    height_of_luminous_area_c0 = safe_float(f.readline().strip())
    height_of_luminous_area_c90 = safe_float(f.readline().strip())
    height_of_luminous_area_c180 = safe_float(f.readline().strip())
    height_of_luminous_area_c270 = safe_float(f.readline().strip())
    dff_percent = safe_float(f.readline().strip())
    lor_percent = safe_float(f.readline().strip())
    conversion_factor = safe_float(f.readline().strip())
    tilt = safe_float(f.readline().strip())
    number_of_lamp_sets = safe_int(f.readline().strip())
    lamp_sets = [extract_lamp_set(f) for _ in range(number_of_lamp_sets)] if number_of_lamp_sets else []
    direct_ratios_for_room_indices = [safe_float(f.readline().strip()) for _ in range(10)]
    c_angles = [safe_float(f.readline().strip()) for _ in range(number_of_c_planes)] if number_of_c_planes else []
    gamma_angles = [safe_float(f.readline().strip()) for _ in range(number_of_intensities)] if number_of_intensities else []

    intensities = extract_intensities(
        f,
        symmetry=symmetry_indicator,
        num_c=number_of_c_planes,
        num_gamma=number_of_intensities
    )

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

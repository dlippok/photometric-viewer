from typing import IO

from photometric_viewer.model.photometry import Photometry, LuminousOpening, LuminousOpeningShape, Lamps, \
    PhotometryMetadata


def _create_luminous_opening(opening_length, opening_width) -> LuminousOpening:
    return LuminousOpening(
        length=opening_length,
        width=opening_width or opening_length,
        shape=LuminousOpeningShape.RECTANGULAR if opening_width > 0 else LuminousOpeningShape.ROUND
    )

def import_from_file(f: IO):
    manufacturer = f.readline().strip()
    light_source_type = int(f.readline().strip())
    symmetry = int(f.readline().strip())
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
    correction_factor = float(f.readline().strip())
    tilt = float(f.readline().strip())
    no_lamp_sets = int(f.readline().strip())

    lamp_sets = []
    for _ in range(no_lamp_sets):
        no_lamps = int(f.readline().strip())
        lamp_sets.append({
                "number_of_lamps": abs(no_lamps),
                "type": f.readline().strip(),
                "luminous_flux": float(f.readline().strip()),
                "color": f.readline().strip(),
                "cri": int(f.readline().strip()),
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

    if symmetry == 0:
        for c in c_angles:
            for gamma in gamma_angles:
                raw_value = float(f.readline().strip())
                print(c, gamma, raw_value)
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == 1:
        for gamma in gamma_angles:
            raw_value = float(f.readline().strip())
            for c in c_angles:
                print(c, gamma, raw_value)
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == 2:
        for c in c_angles:
            if c <= 90:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(90-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
            if c >= 270:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(270-(c-270), gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == 3:
        for c in c_angles:
            if c <= 180:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    if c not in (0, 180):
                        values[(360-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == 4:
        for c in c_angles:
            if c <= 90:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(360-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(180-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(180+c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value

    f.seek(0)
    source = f.read()

    return Photometry(
        is_absolute=is_absolute,
        v_angles=gamma_angles,
        h_angles=c_angles,
        c_values=values,
        luminous_opening=_create_luminous_opening(opening_length, opening_width),
        lamps=[Lamps(
            number_of_lamps=lamps["number_of_lamps"],
            lumens_per_lamp=lamps["luminous_flux"] / lamps["number_of_lamps"],
            is_absolute=is_absolute,
            wattage=lamps["wattage"],
            color=lamps["color"],
            cri=lamps["cri"],
            description=None,
            catalog_number=None,
            position=None,
        ) for lamps in lamp_sets],
        ballast=None,
        metadata=PhotometryMetadata(
            catalog_number=luminaire_catalog_number,
            luminaire=luminaire_name,
            manufacturer=manufacturer,
            file_source=source,
            additional_properties={
                "Measurement": measurement,
                "Filename": filename,
                "Date and user": date_and_user,

            }
        )
    )

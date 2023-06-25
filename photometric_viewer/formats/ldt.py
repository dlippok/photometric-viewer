from typing import IO

from photometric_viewer.model.photometry import Photometry, LuminousOpeningGeometry, Shape, Lamps, \
    PhotometryMetadata, LuminaireGeometry
from photometric_viewer.model.units import LengthUnits

def _create_luminous_opening(length, width) -> LuminousOpeningGeometry:
    return LuminousOpeningGeometry(
        length=length,
        width=width or length,
        shape=Shape.RECTANGULAR if width > 0 else Shape.ROUND
    )


def _create_luminaire_geometry(length, width, height) -> LuminaireGeometry:
    return LuminaireGeometry(
        length=length,
        width=width or length,
        height=height,
        shape=Shape.RECTANGULAR if width > 0 else Shape.ROUND
    )


def _get_source_type(light_source_type: int):
    match light_source_type:
        case 1: return _("Point source with symmetry about the vertical axis")
        case 2: return _("Linear luminaire")
        case 3: return _("Point source with any other symmetry")


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
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == 1:
        for gamma in gamma_angles:
            raw_value = float(f.readline().strip())
            for c in c_angles:
                values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == 2:
        for c in c_angles:
            if c <= 180:
                for gamma in gamma_angles:
                    raw_value = float(f.readline().strip())
                    values[(c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
                    values[(360-c, gamma)] = raw_value * lamp_sets[0]["luminous_flux"] / 1000 if is_absolute else raw_value
    elif symmetry == 3:
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
        dff=dff,
        lorl=lorl,
        luminous_opening_geometry=_create_luminous_opening(opening_length, opening_width),
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
            additional_properties={
                _("Luminaire type"): _get_source_type(light_source_type),
                _("Measurement"): measurement,
                _("Filename"): filename,
                _("Date and user"): date_and_user,
                _("Conversion factor for luminous intensities"): conversion_factor
            }
        )
    )

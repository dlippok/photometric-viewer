import csv
import io

from photometric_viewer.model.luminaire import Luminaire


def export_photometry(luminaire: Luminaire):
    header = ["Gamma"] + [f"C{plane:.0f}" for plane in luminaire.c_planes]

    string_io = io.StringIO()
    writer = csv.DictWriter(string_io, fieldnames=header)
    writer.writeheader()

    for gamma_angle in luminaire.gamma_angles:
        row = {"Gamma": gamma_angle} | {
            f"C{c_plane:.0f}": luminaire.intensity_values[(c_plane, gamma_angle)]
            for c_plane in luminaire.c_planes
        }
        writer.writerow(row)

    return string_io.getvalue()

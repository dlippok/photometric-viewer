import csv
import io

from photometric_viewer.model.photometry import Photometry


def export_photometry(photometry: Photometry):
    header = ["Gamma"] + [f"C{plane:.0f}" for plane in photometry.c_planes]

    string_io = io.StringIO()
    writer = csv.DictWriter(string_io, fieldnames=header)
    writer.writeheader()

    for gamma_angle in photometry.gamma_angles:
        row = {"Gamma": gamma_angle} | {
            f"C{c_plane:.0f}": photometry.intensity_values[(c_plane, gamma_angle)]
            for c_plane in photometry.c_planes
        }
        writer.writerow(row)

    return string_io.getvalue()

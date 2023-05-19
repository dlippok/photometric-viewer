from typing import IO

from photometric_viewer.utils.io import read_non_empty_line
from photometric_viewer.formats import ies, ldt


def import_from_file(f: IO):
    possible_ies_header = read_non_empty_line(f)
    f.seek(0)

    photometry = None
    if possible_ies_header.upper().startswith("IESNA"):
        photometry = ies.import_from_file(f)
    else:
        photometry = ldt.import_from_file(f)

    return photometry



from typing import IO

from photometric_viewer.formats import ies, ldt
from photometric_viewer.utils.ioutil import read_non_empty_line
from photometric_viewer.photometry.ies import extractor, converter


def import_from_file(f: IO):
    possible_ies_header = read_non_empty_line(f)
    f.seek(0)

    if possible_ies_header and possible_ies_header.upper().startswith("IESNA"):
        content = extractor.extract_content(f)
        photometry = converter.convert_content(content)
        f.seek(0)
        photometry.metadata.file_source = f.read()
    else:
        photometry = ldt.import_from_file(f)

    return photometry

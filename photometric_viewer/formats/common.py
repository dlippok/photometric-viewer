from typing import IO

from photometric_viewer.formats import ies, ldt
from photometric_viewer.utils.ioutil import first_non_empty_line
from photometric_viewer.photometry.ies95 import extractor as ies95_extractor
from photometric_viewer.photometry.ies95 import converter as ies95_converter
from photometric_viewer.photometry.ies02 import extractor as ies02_extractor
from photometric_viewer.photometry.ies02 import converter as ies02_converter
from photometric_viewer.photometry.ldt import extractor as ldt_extractor
from photometric_viewer.photometry.ldt import converter as ldt_converter


def import_from_file(f: IO):
    possible_ies_header = first_non_empty_line(f)
    f.seek(0)

    if possible_ies_header == "IESNA:LM-63-2002":
        content = ies02_extractor.extract_content(f)
        photometry = ies02_converter.convert_content(content)
        f.seek(0)
        photometry.metadata.file_source = f.read()
    elif possible_ies_header and possible_ies_header.upper().startswith("IESNA"):
        content = ies95_extractor.extract_content(f)
        photometry = ies95_converter.convert_content(content)
        f.seek(0)
        photometry.metadata.file_source = f.read()
    else:
        content = ldt_extractor.extract_content(f)
        converted_content = ldt_converter.convert_content(content)
        f.seek(0)
        converted_content.metadata.file_source = f.read()

        f.seek(0)
        photometry = ldt.import_from_file(f)

        photometry.metadata.file_source = ""
        converted_content.metadata.file_source = ""
        photometry.intensity_values = {}
        converted_content.intensity_values = {}

        if photometry == converted_content:
            print("Both photometries are equal")
        else:

            print("Photometries are not equal")
            print("o", photometry)
            print("c", converted_content)

    return photometry

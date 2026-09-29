from typing import IO

from photometric_viewer.photometry.ies02 import converter as ies02_converter
from photometric_viewer.photometry.ies02 import extractor as ies02_extractor
from photometric_viewer.photometry.ies95 import converter as ies95_converter
from photometric_viewer.photometry.ies95 import extractor as ies95_extractor
from photometric_viewer.photometry.ies91 import converter as ies91_converter
from photometric_viewer.photometry.ies91 import extractor as ies91_extractor
from photometric_viewer.photometry.ldt import converter as ldt_converter
from photometric_viewer.photometry.ldt import extractor as ldt_extractor
from photometric_viewer.utils.ioutil import first_non_empty_line


def import_from_file(f: IO):
    possible_ies_header, _ = first_non_empty_line(f)
    f.seek(0)

    match possible_ies_header:
        case "IESNA:LM-63-2002":
            content = ies02_extractor.extract_content(f)
            return ies02_converter.convert_content(content)
        case "IESNA:LM-63-1995":
            content = ies95_extractor.extract_content(f)
            return ies95_converter.convert_content(content)
        case "IESNA91":
            content = ies91_extractor.extract_content(f)
            return ies91_converter.convert_content(content)
        case _ if possible_ies_header is not None and possible_ies_header.startswith("IESNA"):
            content = ies02_extractor.extract_content(f)
            return ies02_converter.convert_content(content)
        case _:
            content = ldt_extractor.extract_content(f)
            return ldt_converter.convert_content(content)
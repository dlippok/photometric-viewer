from typing import IO

from photometric_viewer.photometry.iesna_common import extractor as iesna_extractor
from photometric_viewer.photometry.ies02 import converter as ies02_converter
from photometric_viewer.photometry.ies02 import validator as ies02_validator
from photometric_viewer.photometry.ies95 import converter as ies95_converter
from photometric_viewer.photometry.ies95 import validator as ies95_validator
from photometric_viewer.photometry.ies91 import converter as ies91_converter
from photometric_viewer.photometry.ies91 import validator as ies91_validator
from photometric_viewer.photometry.ldt import converter as ldt_converter
from photometric_viewer.photometry.ldt import extractor as ldt_extractor
from photometric_viewer.utils.ioutil import first_non_empty_line


def import_from_file(f: IO):
    possible_ies_header, _ = first_non_empty_line(f)
    f.seek(0)

    issues = []

    normalized_header = "".join(ch.lower() for ch in possible_ies_header if ch.isalnum()) if possible_ies_header else ""

    match normalized_header:
        case "iesnalm632002":
            content = iesna_extractor.extract_content(f)
            issues = ies02_validator.validate(content)
            luminaire = ies02_converter.convert_content(content)
        case "iesnalm631995":
            content = iesna_extractor.extract_content(f)
            issues = ies95_validator.validate(content)
            luminaire = ies95_converter.convert_content(content)
        case _ if normalized_header == "iesna91" or normalized_header == "iesnalm631991":
            content = iesna_extractor.extract_content(f)
            issues = ies91_validator.validate(content)
            luminaire = ies91_converter.convert_content(content)
        case _ if normalized_header.startswith("iesna"):
            content = iesna_extractor.extract_content(f)
            issues = ies02_validator.validate(content)
            luminaire = ies02_converter.convert_content(content)
        case _:
            content = ldt_extractor.extract_content(f)
            luminaire = ldt_converter.convert_content(content)

    if issues:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"[{issue.line_number}] [{issue.severity}]: {issue}")
    else:
        print("No issues found")

    return luminaire
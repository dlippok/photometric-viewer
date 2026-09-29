from typing import List

from photometric_viewer.photometry.iesna_common.model import IesContent
from photometry.ies02.validation_issues import Ies02HeaderInvalid
from photometry.validation import ValidationIssueBase


def validate(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    issues.extend(_validate_header(content))

    return issues

def _validate_header(content: IesContent) -> List[Ies02HeaderInvalid]:
    if content.header != "IESNA:LM-63-2002":
        return [Ies02HeaderInvalid(header=content.header, line_number=1)]
    return []
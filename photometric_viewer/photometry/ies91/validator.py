import math
from typing import List

from photometric_viewer.photometry.ies91.validation_issues import Ies91LuminousOpeningGeometryInvalid, \
    Ies91HAnglesTypeCLastValueInvalid, Ies91HAnglesTypeCFirstValueInvalid, \
    Ies91HAnglesTypeBFirstValueInvalid, Ies91HAnglesTypeBLastValueInvalid, Ies91HeaderInvalid, \
    Ies91MetadataKeyMissingRequired, Ies91HAnglesTypeAFirstValueInvalid, Ies91HAnglesTypeALastValueInvalid
from photometric_viewer.photometry.iesna_common.model import IesContent
from photometric_viewer.photometry.common import Attribute
from photometric_viewer.photometry.iesna_common.validator import validate as iesna_common_validate
from photometric_viewer.photometry.validation import (
    AttributeMissingValue,
    ValidationIssueBase, AttributeInvalidValue, NumericAttributeOutOfRange, Severity,
)
from photometric_viewer.utils.conversion import safe_float, safe_int


def validate(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = iesna_common_validate(content)

    issues.extend(_validate_header(content))
    issues.extend(_validate_metadata(content))
    issues.extend(_validate_numeric_attribute("ballast_lamp_photometric_factor", content.lamp_attributes.ballast_lamp_photometric_factor, min_value=0.00001))
    issues.extend(_validate_luminous_opening_geometry(content))
    issues.extend(_validate_h_angles(content))

    return issues


def _validate_header(content: IesContent) -> List[Ies91HeaderInvalid]:
    header = content.header or ""
    if header == "IESNA91":
        return []

    normalized_header = "".join(ch.lower() for ch in header if ch.isalnum())
    if normalized_header == "iesnalm631995" or normalized_header == "iesna91":
        return [Ies91HeaderInvalid(header=content.header, line_number=1, severity=Severity.WARNING)]

    return [Ies91HeaderInvalid(header=content.header, line_number=1, severity=Severity.ERROR)]


def _validate_numeric_attribute(
    name: str,
    attribute: Attribute | None,
    int_value: bool = False,
    min_value: int | float | None = None,
    max_value: int | float | None = None,
    allowed_values: List[int] | None = None
) -> List[ValidationIssueBase]:
    issues = []

    if attribute is None:
        return [AttributeMissingValue(name, None)]
    if attribute.value is None:
        return [AttributeMissingValue(name, attribute.line)]

    if int_value:
        parsed_value = safe_int(attribute.value)
        if parsed_value is None:
            return [AttributeInvalidValue(name, attribute.value, attribute.line)]
    else:
        parsed_value = safe_float(attribute.value)
        if parsed_value is None or not math.isfinite(parsed_value):
            return [AttributeInvalidValue(name, attribute.value, attribute.line)]

    if allowed_values is not None and parsed_value in allowed_values:
        return []
    if min_value is not None and parsed_value < min_value:
        issues.append(NumericAttributeOutOfRange(name, parsed_value, attribute.line, min_value=min_value, max_value=max_value))
    if max_value is not None and parsed_value > max_value:
        issues.append(NumericAttributeOutOfRange(name, parsed_value, attribute.line, min_value=min_value, max_value=max_value))

    return issues

def _validate_metadata(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []

    REQUIRED_METADATA_KEYS = [
        "TEST",
        "MANUFAC",
    ]

    present_keys = [m.key.upper().strip() for m in content.metadata]
    line_number = (content.metadata[-1].line + 1) if content.metadata else 2

    for key in REQUIRED_METADATA_KEYS:
        if key not in present_keys:
            issues.append(Ies91MetadataKeyMissingRequired(key, line_number=line_number))

    return issues

def _sign(value: float | int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0

def _validate_luminous_opening_geometry(content: IesContent) -> List[ValidationIssueBase]:
    ia = content.inline_attributes
    width_attr = ia.luminous_opening_width
    length_attr = ia.luminous_opening_length
    height_attr = ia.luminous_opening_height

    if width_attr.value is None or length_attr.value is None or height_attr.value is None:
        return []

    width = safe_float(width_attr.value)
    length = safe_float(length_attr.value)
    height = safe_float(height_attr.value)

    if width is None or length is None or height is None:
        return []

    valid_combinations = {
        (0, 0, 0),
        (1, 1, 1),
        (-1, 0, 0),
        (-1, 0, -1),
        (-1, 0, 0),
        (0, 1, -1),
        (1, 0, -1),
        (-1, 1, 1),
        (1, -1, 1),
        (-1, 1, -1),
        (1, -1, -1),

    }

    if (_sign(width), _sign(length), _sign(height)) not in valid_combinations:
        line_number = max(attr.line for attr in [width_attr, length_attr, height_attr] if attr is not None)
        return [Ies91LuminousOpeningGeometryInvalid(width, length, height, line_number)]

    return []


def _validate_h_angles(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    if not content.h_angles:
        return issues

    photometry_type = safe_int(content.inline_attributes.photometry_type.value if content.inline_attributes.photometry_type else None)
    parsed_angles: list[tuple[float, int, str]] = []

    if not parsed_angles:
        return issues

    first_value, first_line, _ = parsed_angles[0]
    last_value, last_line, _ = parsed_angles[-1]

    if photometry_type == 1:
        if first_value == 0.0:
            if last_value not in (0.0, 90.0, 180.0, 360.0):
                issues.append(Ies91HAnglesTypeCLastValueInvalid(first_value, last_value, last_line))
        elif first_value == 90.0:
            if last_value != 270.0:
                issues.append(Ies91HAnglesTypeCLastValueInvalid(first_value, last_value, last_line))
        else:
            issues.append(Ies91HAnglesTypeCFirstValueInvalid(first_value, first_line))

    elif photometry_type in (2, 3):
        valid_first_values = (-90.0, 0.0)
        if first_value not in valid_first_values:
            issues.append(Ies91HAnglesTypeBFirstValueInvalid(first_value, first_line) if photometry_type == 2 else Ies91HAnglesTypeAFirstValueInvalid(first_value, first_line))
        if last_value != 90.0:
            issues.append(Ies91HAnglesTypeBLastValueInvalid(last_value, last_line) if photometry_type == 2 else Ies91HAnglesTypeALastValueInvalid(last_value, last_line))

    return issues

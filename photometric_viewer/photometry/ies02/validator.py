import math
from typing import List

from photometric_viewer.photometry.iesna_common.model import IesContent
from photometric_viewer.photometry.common import Attribute
from photometric_viewer.photometry.validation import (
    AttributeMissingValue,
    Severity,
    ValidationIssueBase,
)
from photometric_viewer.utils.conversion import safe_float, safe_int
from photometric_viewer.photometry.iesna_common.validator import validate as iesna_common_validate
from photometric_viewer.photometry.ies02.validation_issues import Ies02HeaderInvalid, \
    Ies02BallastLampPhotometricFactorDeprecated, Ies02MetadataKeyDeprecated, Ies02MetadataUserKeyWithoutUnderscore, \
    Ies02MetadataNearfieldInvalidValue, Ies02MetadataMaintcatInvalidValue, Ies02MetadataFlashareaNotPositive, \
    Ies02MetadataFlashareaUnusualSize, Ies02MetadataFlashareaNotNumber, Ies02LampPositionTwoValuesExpected, \
    Ies02LampPositionHorizontalOutOfRange, Ies02LampPositionVerticalOutOfRange, Ies02LampPositionNotNumbers, Ies02MetadataKeyMissingRequired, \
    Ies02MetadataKeyMissingSuggested, Ies02LuminousOpeningGeometryInvalid, Ies02HAnglesTypeCFirstValueInvalid, \
    Ies02HAnglesTypeCLastValueInvalid, Ies02HAnglesTypeBFirstValueInvalid, Ies02HAnglesTypeAFirstValueInvalid, \
    Ies02HAnglesTypeALastValueInvalid, Ies02HAnglesTypeBLastValueInvalid

def validate(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = iesna_common_validate(content)

    issues.extend(_validate_header(content))
    issues.extend(_validate_metadata(content))
    issues.extend(_validate_future_use_attribute(content.lamp_attributes.ballast_lamp_photometric_factor))
    issues.extend(_validate_luminous_opening_geometry(content))
    issues.extend(_validate_h_angles(content))

    return issues


def _validate_header(content: IesContent) -> List[Ies02HeaderInvalid]:
    header = content.header or ""
    if header == "IESNA:LM-63-2002":
        return []

    normalized_header = "".join(ch.lower() for ch in header if ch.isalnum())
    if normalized_header == "iesnalm632002":
        return [Ies02HeaderInvalid(header=content.header, line_number=1, severity=Severity.WARNING)]

    return [Ies02HeaderInvalid(header=content.header, line_number=1, severity=Severity.ERROR)]


def _validate_future_use_attribute(attribute: Attribute | None) -> List[ValidationIssueBase]:
    if attribute is None:
        return [AttributeMissingValue("future_use", None)]
    if attribute.value is None:
        return [AttributeMissingValue("future_use", attribute.line)]

    parsed_value = safe_float(attribute.value)

    if parsed_value is None or parsed_value != 1.0:
        return [Ies02BallastLampPhotometricFactorDeprecated(attribute.value, attribute.line)]
    return []


def _validate_metadata(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []

    STANDARD_METADATA_KEYS = [
        "TEST",
        "TESTLAB",
        "TESTDATE",
        "NEARFIELD",
        "MANUFAC",
        "LUMCAT",
        "LUMINAIRE",
        "LAMPCAT",
        "LAMP",
        "BALLASTCAT",
        "BALLAST",
        "MAINTCAT",
        "DISTRIBUTION",
        "FLASHAREA",
        "COLORCONSTANT",
        "LAMPPOSITION",
        "ISSUEDATE",
        "SEARCH",
        "OTHER",
        "MORE",
    ]

    seen_keys: dict[str, int] = {}
    for metadata in content.metadata:
        key = metadata.key.strip()
        seen_keys[key.upper()] = seen_keys.get(key.upper(), 0) + 1

    for metadata in content.metadata:
        key = metadata.key.strip().upper()

        if key in ["BLOCK", "ENDBLOCK"]:
            issues.append(Ies02MetadataKeyDeprecated(key, metadata.line))
        if key == "DATE":
            issues.append(Ies02MetadataKeyDeprecated(key, metadata.line, replaced_by="ISSUEDATE"))

        if not key.startswith("_") and key not in STANDARD_METADATA_KEYS:
            issues.append(Ies02MetadataUserKeyWithoutUnderscore(metadata, metadata.line))

        if key == "NEARFIELD":
            if metadata.value not in ["D1", "D2", "D3"]:
                issues.append(Ies02MetadataNearfieldInvalidValue(metadata, metadata.line))

        if key == "MAINTCAT":
            if metadata.value not in ["1", "2", "3", "4", "5", "6"]:
                issues.append(Ies02MetadataMaintcatInvalidValue(metadata, metadata.line))

        if key == "FLASHAREA":
            try:
                flasharea_value = float(metadata.value)
                if flasharea_value <= 0:
                    issues.append(Ies02MetadataFlashareaNotPositive(metadata, metadata.line))
                if not (0.01 <= flasharea_value <= 2.5):
                    issues.append(Ies02MetadataFlashareaUnusualSize(metadata, metadata.line))
            except ValueError:
                issues.append(Ies02MetadataFlashareaNotNumber(metadata, metadata.line))

        if key == "LAMPPOSITION":
            positions = metadata.value.split(",") if "," in metadata.value else metadata.value.split(" ")

            if len(positions) != 2:
                issues.append(Ies02LampPositionTwoValuesExpected(metadata, metadata.line))
            else:
                try:
                    positions = [float(pos.strip()) for pos in positions]
                    if positions[0] < 0 or positions[0] >= 365:
                        issues.append(Ies02LampPositionHorizontalOutOfRange(metadata, positions[0], metadata.line))
                    if positions[1] < 0 or positions[1] > 180:
                        issues.append(Ies02LampPositionVerticalOutOfRange(metadata, positions[1], metadata.line))
                except ValueError:
                    issues.append(Ies02LampPositionNotNumbers(metadata, metadata.line))

    present_keys = [m.key.upper().strip() for m in content.metadata]
    line_number = (content.metadata[-1].line + 1) if content.metadata else 2

    for key in ["TEST", "TESTLAB", "MANUFAC"]:
        if key not in present_keys:
            issues.append(Ies02MetadataKeyMissingRequired(key, line_number=line_number))

    if "ISSUEDATE" not in present_keys and "DATE" not in present_keys:
        issues.append(Ies02MetadataKeyMissingRequired("ISSUEDATE", line_number=line_number))

    for key in ["LUMCAT", "LUMINAIRE", "LAMPCAT", "LAMP"]:
        if key not in present_keys:
            issues.append(Ies02MetadataKeyMissingSuggested(key, line_number=line_number))

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
        (1, 1, 0),
        (1, 1, 1),
        (-1, -1, 0),
        (-1, -1, 1),
        (-1, -1, -1),
        (-1, 1, -1),
        (1, -1, -1),
        (-1, 0, -1),
    }

    if (_sign(width), _sign(length), _sign(height)) not in valid_combinations:
        line_number = max(attr.line for attr in [width_attr, length_attr, height_attr] if attr is not None)
        return [Ies02LuminousOpeningGeometryInvalid(width, length, height, line_number)]

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
        if first_value != 0.0:
            issues.append(Ies02HAnglesTypeCFirstValueInvalid(first_value, first_line))
        if last_value not in (0.0, 90.0, 180.0, 360.0):
            issues.append(Ies02HAnglesTypeCLastValueInvalid(last_value, last_line))
    elif photometry_type == 2:
        valid_first_values = (-90.0, 0.0)
        if first_value not in valid_first_values:
            issues.append(Ies02HAnglesTypeBFirstValueInvalid(first_value, first_line))
        if last_value != 90.0:
            issues.append(Ies02HAnglesTypeBLastValueInvalid(last_value, last_line))
    elif photometry_type == 3:
        valid_first_values = (-90.0, 0.0)
        if first_value not in valid_first_values:
            issues.append(Ies02HAnglesTypeAFirstValueInvalid(first_value, first_line))
        if last_value != 90.0:
            issues.append(Ies02HAnglesTypeALastValueInvalid(last_value, last_line))

    return issues

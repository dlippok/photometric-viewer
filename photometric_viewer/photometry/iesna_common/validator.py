import math
from typing import List

from photometric_viewer.photometry.iesna_common.model import IesContent
from photometric_viewer.photometry.common import Attribute
from photometric_viewer.photometry.iesna_common.validation_issues import (
    IesMetadataKeyMissing,
    IesMetadataKeyNotUppercase, IesMetadataKeyTooLong, IesMetadataKeyLeadingTrailingWhitespace,
    IesMetadataKeyInvalidCharacters, IesMetadataValueMissing, IesMetadataKeyDuplicate, IesHAnglesValueNotNumber,
    IesHAnglesValueOutOfOrder, IesVAnglesValueNotNumber, IesVAnglesValueOutOfOrder, IesVAnglesTypeCFirstValueInvalid,
    IesVAnglesTypeCLastValueInvalid, IesVAnglesTypeBFirstValueInvalid, IesVAnglesTypeBLastValueInvalid,
    IesVAnglesTypeAFirstValueInvalid, IesVAnglesTypeALastValueInvalid, IesNumberOfIntensitiesInvalid,
    IesIntensityValueNotNumber, IesIntensityValueNegative,
)
from photometric_viewer.photometry.validation import (
    AttributeInvalidValue,
    AttributeMissingValue,
    NumericAttributeOutOfRange,
    ValidationIssueBase,
)
from photometric_viewer.utils.conversion import safe_float, safe_int


def validate(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    issues.extend(_validate_metadata(content))
    issues.extend(_validate_inline_attributes(content))
    issues.extend(_validate_h_angles(content))
    issues.extend(_validate_v_angles(content))
    issues.extend(_validate_intensities(content))
    return issues



def _validate_enum_attribute(
        name: str,
        attribute: Attribute | None,
        allowed_values: List[str] | None = None
) -> List[ValidationIssueBase]:
    if attribute is None:
        return [AttributeMissingValue(name, None)]
    if attribute.value is None:
        return [AttributeMissingValue(name, attribute.line)]
    if allowed_values is None:
        return []
    if attribute.value not in allowed_values:
        return [AttributeInvalidValue(name, attribute.value, attribute.line)]
    return []

def _validate_future_use_attribute(attribute: Attribute | None) -> List[ValidationIssueBase]:
    if attribute is None:
        return [AttributeMissingValue("future_use", None)]
    if attribute.value is None:
        return [AttributeMissingValue("future_use", attribute.line)]

    parsed_value = safe_float(attribute.value)

    if parsed_value is None or parsed_value != 1.0:
        return [AttributeInvalidValue("future_use", attribute.value, attribute.line)]
    return []


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

    seen_keys: dict[str, int] = {}
    for metadata in content.metadata:
        key = metadata.key.strip()
        seen_keys[key.upper()] = seen_keys.get(key.upper(), 0) + 1

    for metadata in content.metadata:
        if not metadata.key:
            issues.append(IesMetadataKeyMissing(metadata, metadata.line))
        if not metadata.key.isupper():
            issues.append(IesMetadataKeyNotUppercase(metadata, metadata.line))
        if len(metadata.key) > 18:
            issues.append(IesMetadataKeyTooLong(metadata, metadata.line))
        if metadata.key.strip() != metadata.key:
            issues.append(IesMetadataKeyLeadingTrailingWhitespace(metadata, metadata.line))

        key = metadata.key.strip().upper()
        for c in key:
            if not c.isalnum() and c != "_":
                issues.append(IesMetadataKeyInvalidCharacters(metadata, metadata.line))
                break

        if not metadata.value and metadata.key not in ["MORE"]:
            issues.append(IesMetadataValueMissing(metadata, metadata.line))

        if seen_keys.get(key, 0) > 1 and key not in ["MORE", "OTHER"]:
            issues.append(IesMetadataKeyDuplicate(metadata, metadata.line))
    return issues


def _validate_inline_attributes(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    ia = content.inline_attributes
    la = content.lamp_attributes

    x = _validate_numeric_attribute("number_of_lamps", ia.number_of_lamps, int_value=True, min_value=1)
    issues.extend(x)

    x = _validate_numeric_attribute("lumens_per_lamp", ia.lumens_per_lamp, int_value=False, min_value=1, allowed_values=[-1])
    issues.extend(x)

    x = _validate_numeric_attribute("multiplying_factor", ia.multiplying_factor, min_value=0.0001)
    issues.extend(x)

    x = _validate_numeric_attribute("n_v_angles", ia.n_v_angles, int_value=True, min_value=1)
    issues.extend(x)

    x = _validate_numeric_attribute("n_h_angles", ia.n_h_angles, int_value=True, min_value=1)
    issues.extend(x)

    x = _validate_enum_attribute("photometry_type", ia.photometry_type, ["1", "2", "3"])
    issues.extend(x)

    x = _validate_enum_attribute("luminous_opening_units", ia.luminous_opening_units, ["1", "2"])
    issues.extend(x)

    x = _validate_numeric_attribute("luminous_opening_width", ia.luminous_opening_width)
    issues.extend(x)

    x = _validate_numeric_attribute("luminous_opening_length", ia.luminous_opening_length)
    issues.extend(x)

    x = _validate_numeric_attribute("luminous_opening_height", ia.luminous_opening_height)
    issues.extend(x)

    x = _validate_numeric_attribute("ballast_factor", la.ballast_factor, min_value=0.0001)
    issues.extend(x)

    x = _validate_numeric_attribute("input_watts", la.input_watts, min_value=0.0001)
    issues.extend(x)

    return issues

def _validate_h_angles(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    if not content.h_angles:
        return issues

    parsed_angles: list[tuple[float, int, str]] = []

    for angle in content.h_angles:
        value = safe_float(angle.value)
        if value is None or not math.isfinite(value):
            issues.append(IesHAnglesValueNotNumber(angle.value, angle.line))
            continue
        parsed_angles.append((value, angle.line, angle.value))

    if not parsed_angles:
        return issues

    for index in range(1, len(parsed_angles)):
        previous_value, _, _ = parsed_angles[index - 1]
        current_value, current_line, _ = parsed_angles[index]
        if current_value < previous_value:
            issues.append(IesHAnglesValueOutOfOrder(current_value, current_line))

    return issues

def _validate_v_angles(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    if not content.v_angles:
        return issues

    photometry_type = safe_int(content.inline_attributes.photometry_type.value if content.inline_attributes.photometry_type else None)
    parsed_angles: list[tuple[float, int, str]] = []

    for angle in content.v_angles:
        value = safe_float(angle.value)
        if value is None or not math.isfinite(value):
            issues.append(IesVAnglesValueNotNumber(angle.value, angle.line))
            continue
        parsed_angles.append((value, angle.line, angle.value))

    if len(parsed_angles) < 2:
        return issues

    for index in range(1, len(parsed_angles)):
        previous_value, _, _ = parsed_angles[index - 1]
        current_value, current_line, _ = parsed_angles[index]
        if current_value < previous_value:
            issues.append(IesVAnglesValueOutOfOrder(current_value, current_line))

    first_value, first_line, _ = parsed_angles[0]
    last_value, last_line, _ = parsed_angles[-1]

    if photometry_type == 1:
        if first_value not in (0.0, 90.0):
            issues.append(IesVAnglesTypeCFirstValueInvalid(first_value, first_line))
        if last_value not in (90.0, 180.0):
            issues.append(IesVAnglesTypeCLastValueInvalid(last_value, last_line))
    elif photometry_type == 2:
        if first_value not in (-90.0, 0.0):
            issues.append(IesVAnglesTypeBFirstValueInvalid(first_value, first_line))
        if last_value != 90.0:
            issues.append(IesVAnglesTypeBLastValueInvalid(last_value, last_line))
    elif photometry_type == 3:
        if first_value not in (-90.0, 0.0):
            issues.append(IesVAnglesTypeAFirstValueInvalid(first_value, first_line))
        if last_value != 90.0:
            issues.append(IesVAnglesTypeALastValueInvalid(last_value, last_line))

    return issues


def _validate_intensities(content: IesContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []

    n_v_angles = safe_int(content.inline_attributes.n_v_angles and content.inline_attributes.n_v_angles.value) or 0
    n_h_angles = safe_int(content.inline_attributes.n_h_angles and content.inline_attributes.n_h_angles.value) or 0

    expected_block_size = n_v_angles * n_h_angles
    actual_count = len(content.intensities)

    match actual_count:
        case 0 if expected_block_size > 0:
            issues.append(IesNumberOfIntensitiesInvalid(actual_count, expected_block_size))
        case _ if actual_count > expected_block_size:
            line_number = content.intensities[expected_block_size].line
            issues.append(IesNumberOfIntensitiesInvalid(actual_count, expected_block_size, line_number))
        case _ if actual_count < expected_block_size:
            line_number = content.intensities[-1].line
            issues.append(IesNumberOfIntensitiesInvalid(actual_count, expected_block_size, line_number))

    for intensity in content.intensities:
        numeric_value = safe_float(intensity.value)
        if numeric_value is None or not math.isfinite(numeric_value):
            issues.append(IesIntensityValueNotNumber(value=intensity.value, line_number=intensity.line))
            continue
        if numeric_value < 0:
            issues.append(IesIntensityValueNegative(value=intensity.value, line_number=intensity.line))

    return issues
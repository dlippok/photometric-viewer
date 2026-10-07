import math
from typing import List

from photometric_viewer.photometry.common import Attribute
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet
from photometric_viewer.photometry.validation import (
    AttributeInvalidValue,
    AttributeMissingValue,
    AttributeTooLong,
    NumericAttributeOutOfRange,
    Severity,
    ValidationIssueBase,
)
from photometric_viewer.photometry.ldt.validation_issues import (
    LdtLampSetAttributeInvalidValue,
    LdtLampSetAttributeMissingValue,
    LdtLampSetAttributeTooLong,
    LdtLampSetNumericAttributeOutOfRange,
)
from photometric_viewer.utils.conversion import safe_float, safe_int


def validate(content: LdtContent) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []

    _validate_text(issues, "manufacturer", content.header, max_length=78, severity=Severity.WARNING)
    _validate_enum(
        issues,
        "type_indicator",
        content.type_indicator,
        {"1", "2", "3"},
        severity=Severity.WARNING,
    )
    _validate_enum(issues, "symmetry_indicator", content.symmetry_indicator, {"0", "1", "2", "3", "4"})
    _validate_integer(issues, "number_of_c_planes", content.number_of_c_planes, minimum=1)
    _validate_float(issues, "distance_between_c_planes", content.distance_between_c_planes, minimum=0)
    _validate_integer(issues, "number_of_intensities", content.number_of_intensities, minimum=1)
    _validate_float(issues, "distance_between_intensities", content.distance_between_intensities, minimum=0)
    _validate_text(issues, "measurement_report", content.measurement_report, max_length=78, severity=Severity.WARNING)
    _validate_text(issues, "luminaire_name", content.luminaire_name, max_length=78, severity=Severity.WARNING)
    _validate_text(issues, "luminaire_number", content.luminaire_number, max_length=78, severity=Severity.WARNING)
    _validate_text(issues, "file_name", content.file_name, max_length=None, severity=Severity.WARNING)
    _validate_text(issues, "date_and_user", content.date_and_user, max_length=78, severity=Severity.WARNING)
    _validate_float(issues, "length_of_luminaire", content.length_of_luminaire, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "width_of_luminaire", content.width_of_luminaire, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "height_of_luminaire", content.height_of_luminaire, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "length_of_luminous_area", content.length_of_luminous_area, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "width_of_luminous_area", content.width_of_luminous_area, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "height_of_luminous_area_c0", content.height_of_luminous_area_c0, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "height_of_luminous_area_c90", content.height_of_luminous_area_c90, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "height_of_luminous_area_c180", content.height_of_luminous_area_c180, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "height_of_luminous_area_c270", content.height_of_luminous_area_c270, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "dff_percent", content.dff_percent, minimum=0, maximum=100, severity=Severity.WARNING)
    _validate_float(issues, "lor_percent", content.lor_percent, minimum=0, maximum=100, severity=Severity.WARNING)
    _validate_float(issues, "conversion_factor", content.conversion_factor, minimum=0, severity=Severity.WARNING)
    _validate_float(issues, "tilt", content.tilt, minimum=0, severity=Severity.WARNING)
    _validate_integer(issues, "number_of_lamp_sets", content.number_of_lamp_sets, minimum=0)

    c_plane_count = safe_int(content.number_of_c_planes.value)
    intensity_count = safe_int(content.number_of_intensities.value)
    lamp_set_count = safe_int(content.number_of_lamp_sets.value)
    if lamp_set_count is not None and lamp_set_count != len(content.lamp_sets):
        issues.append(
            AttributeInvalidValue("lamp_sets", len(content.lamp_sets), content.number_of_lamp_sets.line)
        )
    for index, lamp_set in enumerate(content.lamp_sets, start=1):
        _validate_lamp_set(issues, index, lamp_set)

    for index, attribute in enumerate(content.direct_ratios_for_room_indices, start=1):
        _validate_float(issues, f"direct_ratio_{index}", attribute, minimum=0, severity=Severity.WARNING)
    if len(content.direct_ratios_for_room_indices) != 10:
        line = content.direct_ratios_for_room_indices[-1].line if content.direct_ratios_for_room_indices else None
        issues.append(
            AttributeInvalidValue("direct_ratios_for_room_indices", len(content.direct_ratios_for_room_indices), line)
        )

    parsed_symmetry = safe_int(content.symmetry_indicator.value)
    measured_plane_count = None
    if c_plane_count is not None and c_plane_count > 0 and parsed_symmetry in (0, 1, 2, 3, 4):
        measured_plane_count = _measured_plane_count(c_plane_count, parsed_symmetry)
        if measured_plane_count is None:
            issues.append(
                AttributeInvalidValue(
                    "number_of_c_planes",
                    content.number_of_c_planes.value,
                    content.number_of_c_planes.line,
                )
            )

    _validate_angles(issues, "c_angles", content.c_angles, minimum=0, maximum=360)
    _validate_angles(issues, "gamma_angles", content.gamma_angles, minimum=0, maximum=180)

    if c_plane_count is not None and len(content.c_angles) != c_plane_count:
        issues.append(AttributeInvalidValue("c_angles", len(content.c_angles), content.number_of_c_planes.line))
    if intensity_count is not None and 0 < intensity_count != len(content.gamma_angles):
        issues.append(AttributeInvalidValue("gamma_angles", len(content.gamma_angles), content.number_of_intensities.line))

    expected_intensities = (
        measured_plane_count * intensity_count
        if measured_plane_count is not None and intensity_count is not None and intensity_count > 0
        else None
    )
    if expected_intensities is not None and len(content.intensities) != expected_intensities:
        issues.append(
            AttributeInvalidValue(
                "intensities",
                len(content.intensities),
                content.intensities[-1].line if content.intensities else None,
            )
        )
    for attribute in content.intensities:
        _validate_float(issues, "intensity", attribute, minimum=0)

    return issues


def _validate_lamp_set(
    issues: List[ValidationIssueBase],
    index: int,
    lamp_set: LampSet,
) -> None:
    _validate_integer(
        issues,
        "number_of_lamps",
        lamp_set.number_of_lamps,
        minimum=-1,
        lamp_set_number=index,
    )
    _validate_text(
        issues,
        "type_of_lamp",
        lamp_set.type_of_lamp,
        max_length=24,
        severity=Severity.WARNING,
        lamp_set_number=index,
    )
    _validate_float(
        issues,
        "total_lumens",
        lamp_set.total_lumens,
        minimum=-1,
        severity=Severity.WARNING,
        lamp_set_number=index,
    )
    _validate_text(
        issues,
        "light_color",
        lamp_set.light_color,
        max_length=16,
        severity=Severity.WARNING,
        lamp_set_number=index,
    )
    _validate_text(
        issues,
        "cri",
        lamp_set.cri,
        max_length=6,
        severity=Severity.WARNING,
        lamp_set_number=index,
    )
    if safe_float(lamp_set.cri.value) is not None:
        _validate_float(
            issues,
            "cri",
            lamp_set.cri,
            minimum=0,
            maximum=100,
            severity=Severity.WARNING,
            lamp_set_number=index,
        )
    _validate_float(
        issues,
        "wattage",
        lamp_set.wattage,
        minimum=-1,
        severity=Severity.WARNING,
        lamp_set_number=index,
    )


def _validate_angles(
    issues: List[ValidationIssueBase],
    name: str,
    angles: List[Attribute],
    minimum: float,
    maximum: float,
) -> None:
    previous_value: float | None = None
    for index, attribute in enumerate(angles):
        _validate_float(issues, name, attribute, minimum=minimum, maximum=maximum)
        value = safe_float(attribute.value)
        if value is None:
            continue
        if not math.isfinite(value):
            continue
        if index == 0 and value != 0:
            issues.append(AttributeInvalidValue(name, attribute.value, attribute.line))
        if previous_value is not None and value <= previous_value:
            issues.append(AttributeInvalidValue(name, attribute.value, attribute.line))
        previous_value = value


def _validate_text(
    issues: List[ValidationIssueBase],
    name: str,
    attribute: Attribute | None,
    max_length: int | None,
    severity: Severity = Severity.ERROR,
    lamp_set_number: int | None = None,
) -> None:
    if attribute is None or attribute.value is None or not attribute.value:
        line_number = attribute.line if attribute else None
        if lamp_set_number is None:
            issues.append(AttributeMissingValue(name, line_number, severity))
        else:
            issues.append(
                LdtLampSetAttributeMissingValue(name, lamp_set_number, line_number, severity)
            )
        return
    if max_length is not None and len(attribute.value) > max_length:
        if lamp_set_number is None:
            issues.append(AttributeTooLong(name, attribute.value, max_length, attribute.line))
        else:
            issues.append(
                LdtLampSetAttributeTooLong(name, attribute.value, max_length, lamp_set_number, attribute.line)
            )


def _validate_float(
    issues: List[ValidationIssueBase],
    name: str,
    attribute: Attribute | None,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
    severity: Severity = Severity.ERROR,
    lamp_set_number: int | None = None,
) -> None:
    if attribute is None or attribute.value is None:
        line_number = attribute.line if attribute else None
        if lamp_set_number is None:
            issues.append(AttributeMissingValue(name, line_number, severity))
        else:
            issues.append(
                LdtLampSetAttributeMissingValue(name, lamp_set_number, line_number, severity)
            )
        return

    value = safe_float(attribute.value)
    if value is None or not math.isfinite(value):
        if lamp_set_number is None:
            issues.append(AttributeInvalidValue(name, attribute.value, attribute.line, severity))
        else:
            issues.append(
                LdtLampSetAttributeInvalidValue(
                    name, attribute.value, lamp_set_number, attribute.line, severity
                )
            )
        return

    if minimum is not None and value < minimum:
        if lamp_set_number is None:
            issues.append(
                NumericAttributeOutOfRange(
                    name, value, attribute.line, min_value=minimum, severity=severity
                )
            )
        else:
            issues.append(
                LdtLampSetNumericAttributeOutOfRange(
                    name,
                    value,
                    lamp_set_number,
                    attribute.line,
                    min_value=minimum,
                    severity=severity,
                )
            )
    if maximum is not None and value > maximum:
        if lamp_set_number is None:
            issues.append(
                NumericAttributeOutOfRange(
                    name, value, attribute.line, max_value=maximum, severity=severity
                )
            )
        else:
            issues.append(
                LdtLampSetNumericAttributeOutOfRange(
                    name,
                    value,
                    lamp_set_number,
                    attribute.line,
                    max_value=maximum,
                    severity=severity,
                )
            )


def _validate_integer(
    issues: List[ValidationIssueBase],
    name: str,
    attribute: Attribute | None,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
    severity: Severity = Severity.ERROR,
    lamp_set_number: int | None = None,
) -> None:
    if attribute is None or attribute.value is None:
        line_number = attribute.line if attribute else None
        if lamp_set_number is None:
            issues.append(AttributeMissingValue(name, line_number, severity))
        else:
            issues.append(
                LdtLampSetAttributeMissingValue(name, lamp_set_number, line_number, severity)
            )
        return

    value = safe_int(attribute.value)
    if value is None:
        if lamp_set_number is None:
            issues.append(AttributeInvalidValue(name, attribute.value, attribute.line, severity))
        else:
            issues.append(
                LdtLampSetAttributeInvalidValue(
                    name, attribute.value, lamp_set_number, attribute.line, severity
                )
            )
        return

    if minimum is not None and value < minimum:
        if lamp_set_number is None:
            issues.append(
                NumericAttributeOutOfRange(
                    name, value, attribute.line, min_value=minimum, severity=severity
                )
            )
        else:
            issues.append(
                LdtLampSetNumericAttributeOutOfRange(
                    name,
                    value,
                    lamp_set_number,
                    attribute.line,
                    min_value=minimum,
                    severity=severity,
                )
            )
    if maximum is not None and value > maximum:
        if lamp_set_number is None:
            issues.append(
                NumericAttributeOutOfRange(
                    name, value, attribute.line, max_value=maximum, severity=severity
                )
            )
        else:
            issues.append(
                LdtLampSetNumericAttributeOutOfRange(
                    name,
                    value,
                    lamp_set_number,
                    attribute.line,
                    max_value=maximum,
                    severity=severity,
                )
            )


def _validate_enum(
    issues: List[ValidationIssueBase],
    name: str,
    attribute: Attribute | None,
    allowed_values: set[str],
    severity: Severity = Severity.ERROR,
) -> None:
    if attribute is None or attribute.value is None:
        issues.append(AttributeMissingValue(name, attribute.line if attribute else None, severity))
        return
    if attribute.value not in allowed_values:
        issues.append(AttributeInvalidValue(name, attribute.value, attribute.line, severity))


def _measured_plane_count(c_plane_count: int, symmetry: int) -> int | None:
    if symmetry == 0:
        return c_plane_count
    if symmetry == 1:
        return 1
    if symmetry == 2:
        return c_plane_count // 2 + 1 if c_plane_count % 2 == 0 else None
    if symmetry == 3:
        return c_plane_count // 2 + 1 if c_plane_count % 4 == 0 else None
    if symmetry == 4:
        return c_plane_count // 4 + 1 if c_plane_count % 4 == 0 else None
    return None

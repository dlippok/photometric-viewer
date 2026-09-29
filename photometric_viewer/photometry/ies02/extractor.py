from typing import IO, List, Tuple, Any

import photometric_viewer
from photometric_viewer.photometry.ies02.model import MetadataTuple, InlineAttributes, LampAttributes, IesContent
from photometric_viewer.utils.conversion import safe_int, safe_float
from photometric_viewer.utils.ioutil import first_non_empty_line, get_n_values, read_till_end
from photometric_viewer.photometry.ies02.validation import *
from photometric_viewer.photometry.validation import ValidationIssueBase, AttributeInvalidValue, \
    NumericAttributeOutOfRange, AttributeMissingValue

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
    "MORE"
]

def extract_content(f: IO) -> IesContent:
    all_issues: List[ValidationIssueBase] = []

    header, curline, issues = _extract_header(f)
    all_issues.extend(issues)

    metadata, curline, issues = _extract_metadata(f, curline)
    all_issues.extend(issues)

    inline_attributes, curline, issues = _extract_inline_attributes(f, curline)
    all_issues.extend(issues)

    lamp_attributes, curline, issues = _extract_lamp_attributes(f, curline)
    all_issues.extend(issues)

    v_angles = _extract_v_angles(f, inline_attributes)
    h_angles = _extract_h_angles(f, inline_attributes)
    intensities = _extract_intensities(f)

    for i in all_issues:
        print(f"{i.line_number} {i.severity}: {str(i)}")

    return IesContent(
        header=header,
        metadata=metadata,
        inline_attributes=inline_attributes,
        lamp_attributes=lamp_attributes,
        v_angles=v_angles,
        h_angles=h_angles,
        intensities=intensities,
        validation_issues=all_issues
    )


def _extract_header(f: IO) -> Tuple[str | None, int, List[ValidationIssueBase]]:
    line, n = first_non_empty_line(f)
    if line is None:
        return None, n, [Ies02HeaderNotFound(None)]

    header = line.strip()
    if header != "IESNA:LM-63-2002":
        return None, n, [Ies02HeaderInvalid(header=header, line_number=n)]
    return header, n, []

def _extract_metadata(f: IO, curline: int) -> Tuple[List[MetadataTuple], int, List[ValidationIssueBase]]:
    metadata: List[MetadataTuple] = []
    validation_issues: List[ValidationIssueBase] = []

    next_line, n = first_non_empty_line(f)
    curline += n
    while next_line and next_line.startswith("["):
        metadata_line = next_line.split("]")
        metadata_key = metadata_line[0].strip("[")
        metadata_value = metadata_line[1].strip()
        t = photometric_viewer.photometry.ies02.model.MetadataTuple(metadata_key, metadata_value)
        tuple_issues = validate_metadata_tuple(t, curline, metadata)
        metadata.append(t)
        validation_issues.extend(tuple_issues)
        next_line, n = first_non_empty_line(f)
        curline += n

    missing_key_issues = validate_metadata_keys(metadata)
    validation_issues.extend(missing_key_issues)
    return metadata, curline, validation_issues

def validate_metadata_tuple(metadata: MetadataTuple, line_number: int, current_metadata: List[MetadataTuple]) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    if not metadata.key:
        issues.append(Ies02MetadataKeyMissing(metadata, line_number))
    if not metadata.key.isupper():
        issues.append(Ies02MetadataKeyNotUppercase(metadata, line_number))
    if len(metadata.key) > 18:
        issues.append(Ies02MetadataKeyTooLong(metadata, line_number))
    if metadata.key.strip() != metadata.key:
        issues.append(Ies02MetadataKeyLeadingTrailingWhitespace(metadata, line_number))

    key = metadata.key.strip().upper()
    for c in key:
        if not c.isalnum() and c not in ["_"]:
            issues.append(Ies02MetadataKeyInvalidCharacters(metadata, line_number))
            break

    if not metadata.value and metadata.key not in ["MORE"]:
        issues.append(Ies02MetadataValueMissing(metadata, line_number))

    if any(m.key.upper().strip() == key for m in current_metadata) and metadata.key not in ["MORE", "OTHER"]:
        issues.append(Ies02MetadataKeyDuplicate(metadata, line_number))

    if key in ["BLOCK", "ENDBLOCK"]:
        issues.append(Ies02MetadataKeyDeprecated(key, line_number))
    if key == "DATE":
        issues.append(Ies02MetadataKeyDeprecated(key, line_number, replaced_by="ISSUEDATE"))

    if not key.startswith("_") and key not in STANDARD_METADATA_KEYS:
        issues.append(Ies02MetadataUserKeyWithoutUnderscore(metadata, line_number))

    if key == 'NEARFIELD':
        if metadata.value not in ['D1', 'D2', 'D3']:
            issues.append(Ies02MetadataNearfieldInvalidValue(metadata, line_number))

    if key == 'MAINTCAT':
        if metadata.value not in ['1', '2', '3', "4", "5", "6"]:
            issues.append(Ies02MetadataMaintcatInvalidValue(metadata, line_number))

    if key == 'FLASHAREA':
        try:
            flasharea_value = float(metadata.value)
            if flasharea_value <= 0:
                issues.append(Ies02MetadataFlashareaNotPositive(metadata, line_number))
            if not(0.01 <= flasharea_value <= 2.5):
                issues.append(Ies02MetadataFlashareaUnusualSize(metadata, line_number))
        except ValueError:
            issues.append(Ies02MetadataFlashareaNotNumber(metadata, line_number))

    if key == 'LAMPPOSITION':
        positions = metadata.value.split(",") if "," in metadata.value else metadata.value.split(" ")

        if len(positions) != 2:
            issues.append(Ies02LampPositionTwoValuesExpected(metadata, line_number))

        try:
            positions = [float(pos.strip()) for pos in positions]
            if positions[0] < 0 or positions[0] >= 365:
                issues.append(Ies02LampPositionOutOfRange(metadata, line_number))
            if positions[1] < 0 or positions[1] > 180:
                issues.append(Ies02LampPositionOutOfRange(metadata, line_number))
        except ValueError:
            issues.append(Ies02LampPositionNotNumbers(metadata, line_number))

    return issues

def validate_metadata_keys(metadata: List[MetadataTuple]) -> List[ValidationIssueBase]:
    issues: List[ValidationIssueBase] = []
    present_keys = [m.key.upper().strip() for m in metadata]

    required_keys = ["TEST", "TESTLAB", "MANUFAC"]
    for key in required_keys:
        if key not in present_keys:
            issues.append(Ies02MetadataKeyMissingRequired(key))

    if "ISSUEDATE" not in present_keys and "DATE" not in present_keys:
        issues.append(Ies02MetadataKeyMissingRequired("ISSUEDATE"))

    suggested_keys = ["LUMCAT", "LUMINAIRE", "LAMPCAT", "LAMP"]
    for key in suggested_keys:
        if key not in present_keys:
            issues.append(Ies02MetadataKeyMissingSuggested(key))

    return issues

def _extract_inline_attributes(f: IO, curline: int) -> tuple[InlineAttributes, int, list[ValidationIssueBase]]:
    raw_attributes = get_n_values(f, 10)
    raw_attributes.reverse()

    issues: List[ValidationIssueBase] = []
    startline = curline

    number_of_lamps, curline, parse_issues = _next_attribute("number_of_lamps", raw_attributes, int, startline, min_value=1)
    issues.extend(parse_issues)

    lumens_per_lamp, curline, parse_issues = _next_attribute("lumens_per_lamp", raw_attributes, float, startline)
    issues.extend(parse_issues)

    if lumens_per_lamp is not None and lumens_per_lamp < 1 and lumens_per_lamp != -1:
        issues.append(NumericAttributeOutOfRange("lumens_per_lamp", lumens_per_lamp, curline, min_value=1))

    multiplying_factor, curline, parse_issues = _next_attribute("multiplying_factor", raw_attributes, float, startline, min_value=0.0001)
    issues.extend(parse_issues)

    n_v_angles, curline, parse_issues = _next_attribute("n_v_angles", raw_attributes, int, startline, min_value=1)
    issues.extend(parse_issues)

    n_h_angles, curline, parse_issues = _next_attribute("n_h_angles", raw_attributes, int, startline, min_value=1)
    issues.extend(parse_issues)

    photometry_type, curline, parse_issues = _next_attribute("photometry_type", raw_attributes, int, startline, allowed_values=[1, 2, 3])
    issues.extend(parse_issues)

    luminous_opening_units, curline, parse_issues = _next_attribute("luminous_opening_units", raw_attributes, int, startline, allowed_values=[1, 2])
    issues.extend(parse_issues)

    luminous_opening_width, curline, parse_issues = _next_attribute("luminous_opening_width", raw_attributes, float, startline)
    issues.extend(parse_issues)

    luminous_opening_length, curline, parse_issues = _next_attribute("luminous_opening_length", raw_attributes, float, startline)
    issues.extend(parse_issues)

    luminous_opening_height, curline, parse_issues = _next_attribute("luminous_opening_height", raw_attributes, float, startline)
    issues.extend(parse_issues)

    attributes = InlineAttributes(
        number_of_lamps=number_of_lamps,
        lumens_per_lamp=lumens_per_lamp,
        multiplying_factor=multiplying_factor,
        n_v_angles=n_v_angles,
        n_h_angles=n_h_angles,
        photometry_type=photometry_type,
        luminous_opening_units=luminous_opening_units,
        luminous_opening_width=luminous_opening_width,
        luminous_opening_length=luminous_opening_length,
        luminous_opening_height=luminous_opening_height
    )

    return attributes, curline, issues


def _extract_lamp_attributes(f: IO, curline: int) -> Tuple[LampAttributes, int, list[ValidationIssueBase]]:
    raw_attributes = get_n_values(f, 3)
    raw_attributes.reverse()
    issues: List[ValidationIssueBase] = []

    startline = curline

    ballast_factor, curline, parse_issues = _next_attribute("ballast_factor", raw_attributes, float, startline, min_value=0.0001)
    issues.extend(parse_issues)

    future_use, curline, parse_issues = _next_attribute("future_use", raw_attributes, float, startline)
    issues.extend(parse_issues)
    if future_use != 1.0:
        issues.append(AttributeInvalidValue("future_use", future_use, curline, severity=Severity.WARNING))

    input_watts, curline, parse_issues = _next_attribute("input_watts", raw_attributes, float, startline, min_value=0.0001)
    issues.extend(parse_issues)

    attributes = LampAttributes(
        ballast_factor=ballast_factor,
        future_use="1",
        input_watts=input_watts
    )
    return attributes, curline, issues


def _extract_v_angles(f: IO, attributes: InlineAttributes) -> List[float]:
    n_angles = attributes.n_v_angles or 0
    raw_angles = get_n_values(f, n_angles)

    return [
        safe_float(angle[0])
        for angle in raw_angles
        if angle[0] is not None
    ]


def _extract_h_angles(f: IO, attributes: InlineAttributes) -> List[float]:
    n_angles = attributes.n_h_angles or 0
    return [
        safe_float(angle[0])
        for angle in get_n_values(f, n_angles)
        if angle[0] is not None
    ]


def _extract_intensities(f: IO) -> List[float]:
    return [
        safe_float(v[0])
        for v in read_till_end(f)
    ]

def _next_attribute(
        name: str,
        values: List[Tuple[str, int]],
        parse_func,
        start_line_number: int,
        min_value: float | int | None = None,
        max_value: float | int | None = None,
        allowed_values: List[Any] | None = None,
        default_value: Any | None = None
) -> Tuple[Any | None, int, List[ValidationIssueBase]]:
    issues: List[ValidationIssueBase] = []

    try:
        value = values.pop()
    except IndexError:
        return default_value, start_line_number, [AttributeMissingValue(name, start_line_number)]

    line_number = start_line_number + value[1]
    try:
        parsed_value = parse_func(value[0]) if value[0] is not None else None
        if parsed_value is None:
            return default_value, line_number, [AttributeMissingValue(name, line_number)]
        else:
            if min_value is not None and parsed_value < min_value:
                issues.append(NumericAttributeOutOfRange(name, parsed_value, line_number, min_value, max_value))
            if max_value is not None and parsed_value > max_value:
                issues.append(NumericAttributeOutOfRange(name, parsed_value, line_number, min_value, max_value))
            if allowed_values is not None and parsed_value not in allowed_values:
                issues.append(AttributeInvalidValue(name, parsed_value, line_number))
            return parsed_value, line_number, issues
    except (ValueError, TypeError):
        return default_value, line_number, [AttributeInvalidValue(name, value, line_number)]


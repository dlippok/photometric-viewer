from typing import IO, List, Tuple

from photometric_viewer.photometry.ies02.model import MetadataTuple, InlineAttributes, LampAttributes, IesContent
from photometric_viewer.utils.conversion import safe_int, safe_float
from photometric_viewer.utils.ioutil import first_non_empty_line, get_n_values, read_till_end
from photometric_viewer.photometry.ies02.validation import *
from photometric_viewer.photometry.validation import ValidationIssueBase

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

    inline_attributes = _extract_inline_attributes(f)
    lamp_attributes = _extract_lamp_attributes(f)
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
        t = MetadataTuple(metadata_key, metadata_value)
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

def _extract_inline_attributes(f: IO) -> InlineAttributes:
    raw_attributes = get_n_values(f, 10)
    return InlineAttributes(
        number_of_lamps=safe_int(raw_attributes[0]),
        lumens_per_lamp=safe_float(raw_attributes[1]),
        multiplying_factor=safe_float(raw_attributes[2]),
        n_v_angles=safe_int(raw_attributes[3]),
        n_h_angles=safe_int(raw_attributes[4]),
        photometry_type=safe_int(raw_attributes[5]),
        luminous_opening_units=safe_int(raw_attributes[6]),
        luminous_opening_width=safe_float(raw_attributes[7]),
        luminous_opening_length=safe_float(raw_attributes[8]),
        luminous_opening_height=safe_float(raw_attributes[9])
    )


def _extract_lamp_attributes(f: IO) -> LampAttributes:
    lamp_attr = get_n_values(f, 3)

    return LampAttributes(
        ballast_factor=safe_float(lamp_attr[0]),
        future_use=lamp_attr[1],
        input_watts=safe_float(lamp_attr[2])
    )


def _extract_v_angles(f: IO, attributes: InlineAttributes) -> List[float]:
    n_angles = attributes.n_v_angles or 0
    return [
        safe_float(angle)
        for angle in get_n_values(f, n_angles)
        if angle is not None
    ]


def _extract_h_angles(f: IO, attributes: InlineAttributes) -> List[float]:
    n_angles = attributes.n_h_angles or 0
    return [
        safe_float(angle)
        for angle in get_n_values(f, n_angles)
        if angle is not None
    ]


def _extract_intensities(f: IO) -> List[float]:
    return [
        safe_float(v)
        for v in read_till_end(f)
    ]

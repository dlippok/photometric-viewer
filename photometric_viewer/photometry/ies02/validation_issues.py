from photometric_viewer.photometry.iesna_common.model import MetadataTuple
from photometric_viewer.photometry.validation import ValidationIssueBase, Severity


class Ies02HeaderNotFound(ValidationIssueBase):
    def __init__(self, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)

    def __str__(self):
        return "IESNA:LM-63-2002 header not found"

class Ies02HeaderInvalid(ValidationIssueBase):
    def __init__(self, header: str | None, line_number: int | None, severity: Severity = Severity.ERROR):
        super().__init__(line_number, severity)
        self.header = header

    def __str__(self) -> str:
        return f"IESNA:LM-63-2002 header invalid: {self.header}"

class Ies02MetadataKeyMissing(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key missing: {self.metadata.key}"

class Ies02MetadataKeyLeadingTrailingWhitespace(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key has leading or trailing whitespace: '{self.metadata.key}'"

class Ies02MetadataValueMissing(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata value missing for key: {self.metadata.key}"

class Ies02MetadataKeyMissingRequired(ValidationIssueBase):
    def __init__(self, missing_key: str, line_number: int | None = None):
        super().__init__(line_number, Severity.WARNING)
        self.missing_key = missing_key

    def __str__(self) -> str:
        return f"Required metadata key missing: {self.missing_key}"

class Ies02MetadataKeyMissingSuggested(ValidationIssueBase):
    def __init__(self, missing_key: str, line_number: int | None = None):
        super().__init__(line_number, Severity.INFO)
        self.missing_key = missing_key

    def __str__(self) -> str:
        return f"Suggested metadata key missing: {self.missing_key}"

class Ies02MetadataKeyDeprecated(ValidationIssueBase):
    def __init__(self, key: str, line_number: int, replaced_by: str | None = None):
        super().__init__(line_number, Severity.WARNING)
        self.key = key
        self.replaced_by = replaced_by

    def __str__(self) -> str:
        return f"Metadata key deprecated: {self.key}"

class Ies02MetadataKeyInvalidCharacters(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key contains invalid characters: {self.metadata.key}"

class Ies02MetadataKeyNotUppercase(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key is not uppercase: {self.metadata.key}"

class Ies02MetadataKeyDuplicate(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key is duplicated: {self.metadata.key}"


class Ies02MetadataKeyTooLong(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key is too long (more than 18 characters): {self.metadata.key}"

class Ies02MetadataUserKeyWithoutUnderscore(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"User-defined metadata key does not start with an underscore: {self.metadata.key}"


class Ies02MetadataNearfieldInvalidValue(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"NEARFIELD metadata value is invalid: {self.metadata.value}"


class Ies02MetadataMaintcatInvalidValue(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"MAINTCAT metadata value is invalid: {self.metadata.value}"

class Ies02MetadataFlashareaNotNumber(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"FLASHAREA metadata value is not a number: {self.metadata.value}"

class Ies02MetadataFlashareaNotPositive(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"FLASHAREA metadata value is not positive: {self.metadata.value}"

class Ies02MetadataFlashareaUnusualSize(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.INFO)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"FLASHAREA metadata value is unusually large or small: {self.metadata.value}"

class Ies02LampPositionTwoValuesExpected(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata value does not contain two values: {self.metadata.value}"

class Ies02LampPositionNotNumbers(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata value does not contain valid numbers: {self.metadata.value}"

class Ies02LampPositionHorizontalOutOfRange(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, value: float, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata
        self.value = value

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata horizontal value is out of range: {self.metadata.value}"

class Ies02LampPositionVerticalOutOfRange(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, value: float, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata
        self.value = value

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata vertical value is out of range: {self.metadata.value}"

class Ies02IntensityValueNotNumber(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Intensity value is not a number: {self.value}"


class Ies02IntensityValueNegative(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Intensity value is negative: {self.value}"


class Ies02VAnglesValueNotNumber(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Vertical angle value is not a number: {self.value}"


class Ies02VAnglesValueOutOfOrder(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Vertical angles are not in ascending order: {self.value}"


class Ies02VAnglesTypeCFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry first vertical angle is invalid: {self.value}. Expected 0 or 90."


class Ies02VAnglesTypeCLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry last vertical angle is invalid: {self.value}. Expected 90 or 180."


class Ies02VAnglesTypeBFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry first vertical angle is invalid: {self.value}. Expected -90 or 0."


class Ies02VAnglesTypeBLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry last vertical angle is invalid: {self.value}. Expected 90."


class Ies02VAnglesTypeAFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry first vertical angle is invalid: {self.value}. Expected -90 or 0."


class Ies02VAnglesTypeALastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry last vertical angle is invalid: {self.value}. Expected 90."


class Ies02HAnglesValueNotNumber(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Horizontal angle value is not a number: {self.value}"


class Ies02HAnglesValueOutOfOrder(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Horizontal angles are not in ascending order: {self.value}"


class Ies02HAnglesTypeCFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry first horizontal angle is invalid: {self.value}. Expected 0."


class Ies02HAnglesTypeCLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry last horizontal angle is invalid: {self.value}. Expected 0, 90, 180, or 360."


class Ies02HAnglesTypeBFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry first horizontal angle is invalid: {self.value}. Expected 0 or -90."


class Ies02HAnglesTypeBLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry last horizontal angle is invalid: {self.value}. Expected 90."


class Ies02HAnglesTypeAFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry first horizontal angle is invalid: {self.value}. Expected 0 or -90."


class Ies02HAnglesTypeALastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry last horizontal angle is invalid: {self.value}. Expected 90."


class Ies02LuminousOpeningGeometryInvalid(ValidationIssueBase):
    def __init__(self, width, length, height, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.width = width
        self.length = length
        self.height = height

    def __str__(self) -> str:
        return (
            "Luminous opening geometry is invalid: "
            f"width={self.width}, length={self.length}, height={self.height}"
        )

class Ies02NumberOfIntensitiesInvalid(ValidationIssueBase):
    def __init__(self, number, expected, line_number: int | None = None):
        super().__init__(line_number, Severity.ERROR)
        self.expected = expected
        self.number = number

    def __str__(self) -> str:
        return f"Number of intensity values invalid (Given: {self.number}, Expected: {self.expected})"

class Ies02BallastLampPhotometricFactorDeprecated(ValidationIssueBase):
    def __init__(self, value, line_number: int | None = None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Ballast-lamp photometric factor is deprecated. Use 1.0 value instead (Given: {self.value})"

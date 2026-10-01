from photometric_viewer.photometry.iesna_common.model import MetadataTuple
from photometric_viewer.photometry.validation import ValidationIssueBase, Severity


class IesMetadataKeyMissing(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key missing: {self.metadata.key}"

class IesMetadataKeyLeadingTrailingWhitespace(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key has leading or trailing whitespace: '{self.metadata.key}'"

class IesMetadataValueMissing(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata value missing for key: {self.metadata.key}"

class IesMetadataKeyMissingRequired(ValidationIssueBase):
    def __init__(self, missing_key: str, line_number: int | None = None):
        super().__init__(line_number, Severity.WARNING)
        self.missing_key = missing_key

    def __str__(self) -> str:
        return f"Required metadata key missing: {self.missing_key}"

class IesMetadataKeyDeprecated(ValidationIssueBase):
    def __init__(self, key: str, line_number: int, replaced_by: str | None = None):
        super().__init__(line_number, Severity.WARNING)
        self.key = key
        self.replaced_by = replaced_by

    def __str__(self) -> str:
        return f"Metadata key deprecated: {self.key}"

class IesMetadataKeyInvalidCharacters(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key contains invalid characters: {self.metadata.key}"

class IesMetadataKeyNotUppercase(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key is not uppercase: {self.metadata.key}"

class IesMetadataKeyDuplicate(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key is duplicated: {self.metadata.key}"


class IesMetadataKeyTooLong(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Metadata key is too long (more than 18 characters): {self.metadata.key}"

class IesMetadataUserKeyWithoutUnderscore(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.WARNING)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"User-defined metadata key does not start with an underscore: {self.metadata.key}"


class IesMetadataNearfieldInvalidValue(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"NEARFIELD metadata value is invalid: {self.metadata.value}"


class IesMetadataMaintcatInvalidValue(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"MAINTCAT metadata value is invalid: {self.metadata.value}"

class IesMetadataFlashareaNotNumber(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"FLASHAREA metadata value is not a number: {self.metadata.value}"

class IesMetadataFlashareaNotPositive(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"FLASHAREA metadata value is not positive: {self.metadata.value}"

class IesMetadataFlashareaUnusualSize(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.INFO)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"FLASHAREA metadata value is unusually large or small: {self.metadata.value}"

class IesLampPositionTwoValuesExpected(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata value does not contain two values: {self.metadata.value}"

class IesLampPositionNotNumbers(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata value does not contain valid numbers: {self.metadata.value}"

class IesLampPositionOutOfRange(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata value is out of range: {self.metadata.value}"

class IesIntensityValueNotNumber(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Intensity value is not a number: {self.value}"


class IesIntensityValueNegative(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Intensity value is negative: {self.value}"


class IesVAnglesValueNotNumber(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Vertical angle value is not a number: {self.value}"


class IesVAnglesValueOutOfOrder(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Vertical angles are not in ascending order: {self.value}"


class IesVAnglesTypeCFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry first vertical angle is invalid: {self.value}. Expected 0 or 90."


class IesVAnglesTypeCLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry last vertical angle is invalid: {self.value}. Expected 90 or 180."


class IesVAnglesTypeBFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry first vertical angle is invalid: {self.value}. Expected -90 or 0."


class IesVAnglesTypeBLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry last vertical angle is invalid: {self.value}. Expected 90."


class IesVAnglesTypeAFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry first vertical angle is invalid: {self.value}. Expected -90 or 0."


class IesVAnglesTypeALastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry last vertical angle is invalid: {self.value}. Expected 90."


class IesHAnglesValueNotNumber(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Horizontal angle value is not a number: {self.value}"


class IesHAnglesValueOutOfOrder(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Horizontal angles are not in ascending order: {self.value}"


class IesHAnglesTypeCFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry first horizontal angle is invalid: {self.value}. Expected 0."


class IesHAnglesTypeCLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry last horizontal angle is invalid: {self.value}. Expected 0, 90, 180, or 360."


class IesHAnglesTypeBFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry first horizontal angle is invalid: {self.value}. Expected 0 or -90."


class IesHAnglesTypeBLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry last horizontal angle is invalid: {self.value}. Expected 90."


class IesHAnglesTypeAFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry first horizontal angle is invalid: {self.value}. Expected 0 or -90."


class IesHAnglesTypeALastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry last horizontal angle is invalid: {self.value}. Expected 90."


class IesLuminousOpeningGeometryInvalid(ValidationIssueBase):
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


class IesNumberOfIntensitiesInvalid(ValidationIssueBase):
    def __init__(self, number: object, expected: object, line_number: int | None = None) -> None:
        super().__init__(line_number, Severity.ERROR)
        self.expected = expected
        self.number = number

    def __str__(self) -> str:
        return f"Number of intensity values invalid (Given: {self.number}, Expected: {self.expected})"


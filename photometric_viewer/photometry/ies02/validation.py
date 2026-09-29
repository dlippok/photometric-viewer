from photometric_viewer.photometry.ies95.model import MetadataTuple
from photometric_viewer.photometry.validation import ValidationIssueBase, Severity


class Ies02HeaderNotFound(ValidationIssueBase):
    def __init__(self, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)

    def __str__(self):
        return "IESNA:LM-63-2002 header not found"

class Ies02HeaderInvalid(ValidationIssueBase):
    def __init__(self, header: str, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
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
    def __init__(self, missing_key: str):
        super().__init__(None, Severity.WARNING)
        self.missing_key = missing_key

    def __str__(self) -> str:
        return f"Required metadata key missing: {self.missing_key}"

class Ies02MetadataKeyMissingSuggested(ValidationIssueBase):
    def __init__(self, missing_key: str):
        super().__init__(None, Severity.INFO)
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

class Ies02LampPositionOutOfRange(ValidationIssueBase):
    def __init__(self, metadata: MetadataTuple, line_number: int):
        super().__init__(line_number, Severity.ERROR)
        self.metadata = metadata

    def __str__(self) -> str:
        return f"LAMPPOSITION metadata value is out of range: {self.metadata.value}"

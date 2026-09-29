from enum import Enum
from typing import Any


class Severity(Enum):
    # Cannot be read or parsed correctly according to the specification.
    # Fallback or default values cannot be defined reliably or the file may not be usable at all.
    # Examples: missing required values, unexpected number of values, invalid value types, invalid value ranges.
    ERROR = 1

    # Not following the official specification but can be reliably read and parsed to derive correct value.
    # Examples: deprecated keys, suggested optional keys missing, values too long or contain special characters.
    WARNING = 2

    # Correct according to the specification but may be unusual or unexpected.
    # Examples: very high or low values, invalid URLs
    INFO = 3

    # Correct according to the specification but does not follow the recommended or configured style
    # Examples: recommended formatting not followed
    STYLE = 4

class ValidationIssueBase:
    def __init__(self, line_number: int | None, severity: Severity):
        self.line_number = line_number
        self.severity = severity

class AttributeMissingValue(ValidationIssueBase):
    def __init__(
            self,
            attribute: str,
            line_number: int | None,
            severity: Severity = Severity.ERROR
    ):
        super().__init__(line_number, severity)
        self.attribute = attribute

    def __str__(self) -> str:
        return f"Missing attribute {self.attribute}"

class AttributeInvalidValue(ValidationIssueBase):
    def __init__(
            self,
            attribute: str,
            value: Any | None,
            line_number: int | None,
            severity: Severity = Severity.ERROR
    ):
        super().__init__(line_number, severity)
        self.attribute = attribute
        self.value = value

    def __str__(self) -> str:
        return f"Invalid value for attribute {self.attribute}: {self.value!r}"


class NumericAttributeOutOfRange(ValidationIssueBase):
    def __init__(
            self,
            attribute: str,
            value: float | int,
            line_number: int | None,
            min_value: float | int | None = None,
            max_value: float | int | None = None
    ):
        super().__init__(line_number, Severity.INFO)
        self.attribute = attribute
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self) -> str:
        if self.min_value is not None and self.max_value is not None:
            return f"{self.attribute} must be between {self.min_value} and {self.max_value}: {self.value}"
        if self.min_value is not None:
            return f"{self.attribute} must be greater than or equal to {self.min_value}: {self.value}"
        if self.max_value is not None:
            return f"{self.attribute} must be less than or equal to {self.max_value}: {self.value}"

        return f"Attribute {self.attribute} is out of the expected range: {self.value}"
from typing import Any

from photometric_viewer.photometry.validation import Severity, ValidationIssueBase


class LdtLampSetAttributeMissingValue(ValidationIssueBase):
    def __init__(
        self,
        attribute: str,
        lamp_set_number: int,
        line_number: int | None,
        severity: Severity = Severity.WARNING,
    ):
        super().__init__(line_number, severity)
        self.attribute = attribute
        self.lamp_set_number = lamp_set_number

    def __str__(self) -> str:
        return f"Missing attribute {self.attribute} in lamp set {self.lamp_set_number}"


class LdtLampSetAttributeInvalidValue(ValidationIssueBase):
    def __init__(
        self,
        attribute: str,
        value: Any | None,
        lamp_set_number: int,
        line_number: int | None,
        severity: Severity = Severity.ERROR,
    ):
        super().__init__(line_number, severity)
        self.attribute = attribute
        self.value = value
        self.lamp_set_number = lamp_set_number

    def __str__(self) -> str:
        return (
            f"Invalid value for attribute {self.attribute} in lamp set "
            f"{self.lamp_set_number}: {self.value!r}"
        )


class LdtLampSetAttributeTooLong(ValidationIssueBase):
    def __init__(
        self,
        attribute: str,
        value: str,
        max_length: int,
        lamp_set_number: int,
        line_number: int | None,
    ):
        super().__init__(line_number, Severity.WARNING)
        self.attribute = attribute
        self.value = value
        self.max_length = max_length
        self.lamp_set_number = lamp_set_number

    def __str__(self) -> str:
        return (
            f"Attribute {self.attribute} in lamp set {self.lamp_set_number} "
            f"exceeds maximum length of {self.max_length}: {self.value!r}"
        )


class LdtLampSetNumericAttributeOutOfRange(ValidationIssueBase):
    def __init__(
        self,
        attribute: str,
        value: float | int,
        lamp_set_number: int,
        line_number: int | None,
        min_value: float | int | None = None,
        max_value: float | int | None = None,
        severity: Severity = Severity.INFO,
    ):
        super().__init__(line_number, severity)
        self.attribute = attribute
        self.value = value
        self.lamp_set_number = lamp_set_number
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self) -> str:
        if self.min_value is not None and self.max_value is not None:
            range_message = f"must be between {self.min_value} and {self.max_value}"
        elif self.min_value is not None:
            range_message = f"must be greater than or equal to {self.min_value}"
        elif self.max_value is not None:
            range_message = f"must be less than or equal to {self.max_value}"
        else:
            range_message = "is out of the expected range"
        return (
            f"{self.attribute} in lamp set {self.lamp_set_number} {range_message}: {self.value}"
        )

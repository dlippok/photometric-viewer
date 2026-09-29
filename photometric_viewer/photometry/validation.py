from enum import Enum

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
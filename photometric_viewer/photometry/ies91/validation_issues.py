from photometric_viewer.photometry.validation import ValidationIssueBase, Severity


class Ies91HeaderInvalid(ValidationIssueBase):
    def __init__(self, header: str | None, line_number: int | None, severity: Severity = Severity.ERROR):
        super().__init__(line_number, severity)
        self.header = header

    def __str__(self) -> str:
        return f"IESNA:LM-63-1991 header invalid: {self.header}"


class Ies91MetadataKeyMissingRequired(ValidationIssueBase):
    def __init__(self, key: str, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.key = key

    def __str__(self) -> str:
        return f"Metadata key '{self.key}' is missing a required value"


class Ies91LuminousOpeningGeometryInvalid(ValidationIssueBase):
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

class Ies91HAnglesTypeCFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type C photometry first horizontal angle is invalid: {self.value}. Expected 0."


class Ies91HAnglesTypeCLastValueInvalid(ValidationIssueBase):
    def __init__(self, first_value, last_value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.first_value = first_value
        self.last_value = last_value

    def __str__(self) -> str:
        if self.first_value == 0:
            return f"Type C photometry last horizontal angle is invalid: {self.last_value}. Expected 90, 180, or 360."
        else:
            return f"Type C photometry last horizontal angle is invalid: {self.last_value}. Expected 270."


class Ies91HAnglesTypeBFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry first horizontal angle is invalid: {self.value}. Expected 0 or -90."


class Ies91HAnglesTypeBLastValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type B photometry last horizontal angle is invalid: {self.value}. Expected 90."


class Ies91HAnglesTypeAFirstValueInvalid(ValidationIssueBase):
    def __init__(self, value, line_number: int | None):
        super().__init__(line_number, Severity.ERROR)
        self.value = value

    def __str__(self) -> str:
        return f"Type A photometry first horizontal angle is invalid: {self.value}. Expected 0 or -90."
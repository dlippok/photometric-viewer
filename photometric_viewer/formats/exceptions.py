class InvalidPhotometricFileFormatException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidLuminousOpeningException(InvalidPhotometricFileFormatException):
    def __init__(self):
        super().__init__(_("Invalid values for luminous opening geometry"))


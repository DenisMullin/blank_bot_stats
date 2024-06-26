class RegistrationError(Exception):
    def __init__(self):
        super().__init__("Failed to register user")


class StructureError(Exception):
    """Exception raised for errors in the structure."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
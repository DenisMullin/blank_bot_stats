class RegistrationError(Exception):
    def __init__(self):
        super().__init__("Failed to register user")
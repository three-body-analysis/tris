# Exactly what it says on the tin, please get a person to look at this very cursed system

class GetAHumanException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

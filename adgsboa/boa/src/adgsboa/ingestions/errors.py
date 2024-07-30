"""
Errors definition for the adgsboa module

module adgsboa
"""
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UnrecognizedMission(Error):
    """Exception raised when the mission identifier is not recognized.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class ConfigCannotBeRead(Error):
    """Exception raised when the configuration file cannot be read.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class ConfigDoesNotPassSchema(Error):
    """Exception raised when the configuration does not pass the schema.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

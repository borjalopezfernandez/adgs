"""
Errors definition for the adgsfe module

module adgsfe
"""
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class EnvironmentVariableNotDefined(Error):
    """Exception raised when an environment variable is not defined.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

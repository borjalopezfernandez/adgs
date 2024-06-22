"""
Errors definition for the adgsfe module

module adgsfe
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

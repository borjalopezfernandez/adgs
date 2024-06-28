"""
Errors definition for the ADGS scripts module

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class WrongMetricGeneratorPeriod(Error):
    """Exception raised when the received period to generate metrics has a start value greater than its stop.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class EnvironmentVariableNotDefined(Error):
    """Exception raised when an environment variable is not defined.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

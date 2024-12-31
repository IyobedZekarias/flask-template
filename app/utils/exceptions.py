"""EXCEPTIONS FILE FOR ALL THINGS IN THE API"""


class APPError(Exception):
    """F2R exception handling class"""

    def __init__(self, message: str):
        self.message = message

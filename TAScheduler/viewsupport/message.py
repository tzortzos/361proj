from enum import Enum, auto

class Message:
    """
    Represents a popover message to be shown ot the user on page load.
    """

    class Type(Enum):
        ERROR = auto(),
        REGULAR = auto(),

    def __init__(self, messsage: str, type: Type = Type.REGULAR):
        self._message = messsage
        self._type = type

    def message(self) -> str:
        """Get the value of this popover message"""
        return self._message

    def type(self) -> Type:
        """Get the type of this popover message"""
        return self._type
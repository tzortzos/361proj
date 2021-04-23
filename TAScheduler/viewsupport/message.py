from enum import Enum, auto

class Message:
    """
    Represents a popover message to be shown ot the user on page load.
    """

    class Type(Enum):
        ERROR = auto(),
        REGULAR = auto(),

    def __init__(self, messsage: str, ty: Type = Type.REGULAR):
        self._message = messsage
        self._ty = ty

    def message(self) -> str:
        """Get the value of this popover message"""
        return self._message

    def type(self) -> Type:
        """Get the type of this popover message"""
        return self._ty

    def __eq__(self, other) -> bool:
        if type(other) is not Message:
            return False
        return self._ty.value == other._ty.value and self._message == other._message

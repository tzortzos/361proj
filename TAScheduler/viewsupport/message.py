from enum import Enum, auto
from typing import Iterable, List, Union

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


class MethodQueue:
    """
    Methods for sending messages to the user across application pages.
    Should be drained into view on each page load.
    """

    @staticmethod
    def drain(session) -> Iterable[Message]:
        """Take all messages from the message queue"""
        try:
            messages: List[Message] = session['messages']

            # Clear message queue
            del session['messages']

            return iter(messages)
        except KeyError:
            return iter([])

    @staticmethod
    def drain_n(session, n: int) -> Iterable[Message]:
        """Take up to n messages from the message queue"""
        try:
            messages: List[Message] = session['messages']
            m_len = len(messages)

            # Take n from message queue, or remainder if there are fewer than n left
            if m_len < n:
                del session['messages']
                return iter(messages)
            else:
                session['messages'] = messages[n:]
                return iter(messages[:n])

        except KeyError:
            return iter([])

    @staticmethod
    def push(session, messages: Union[List[Message], Message]):
        """Add a message to the message queue for the next page render"""
        try:
            current: List[Message] = session['messages']
        except KeyError:
            current: List[Message] = []

        if type(messages) is Message:
            session['messages'] = current + [messages]
        else:
            session['messages'] = current + messages
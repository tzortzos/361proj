from __future__ import annotations
from typing import Optional, Union, Generic, TypeVar, Type
from enum import Enum, auto

P = TypeVar('P', bound=Enum)


class PageError(Generic[P]):
    """
    Represents an error which may or may not have a headline, and which should be rendered with the
    `partials/inline_error.html` partial.
    """

    def __init__(self, msg: str, place: P):
        """
        Create a new basic error with or without a headline value
        """
        self._msg = msg
        self._place = place

    def message(self) -> str:
        """Return the message contained in this error"""
        return self._msg

    def place(self) -> P:
        """Return the placement of this error"""
        return self._place



class LoginPlace(Enum):
    USERNAME = 0
    PASSWORD = 1

    def username(self) -> bool:
        return self is LoginPlace.USERNAME

    def password(self) -> bool:
        return self is LoginPlace.PASSWORD


# Export a Concertized variant of PageError for consumption
"""Represents errors that can be displayed on the login page"""
LoginError = PageError[LoginPlace]


class UserEditError:
    """
    Represents error states for the creation and editing of a user.
    """

    class Place(Enum):
        USERNAME = auto()
        PASSWORD = auto()
        TYPE = auto()
        PHONE = auto()

    def __init__(self, error_text: Union[PageError, str], place: Place):
        self._place = place
        if type(error_text) is PageError:
            self._error = error_text
        elif type(error_text) is str:
            self._error = PageError(error_text)
        else:
            raise TypeError('error_text must be either a PageError or str')

    def error(self) -> PageError:
        """Get the inner error from this UserEditError"""
        return self._error

    def place(self):
        """Get the place for this error"""
        return self._place

    def place_username(self) -> bool:
        return self._place == UserEditError.Place.USERNAME

    def place_password(self) -> bool:
        return self._place == UserEditError.Place.PASSWORD

    def place_type(self) -> bool:
        return self._place == UserEditError.Place.TYPE

    def place_phone(self) -> bool:
        return self._place == UserEditError.Place.PHONE


class SectionError:
    """
    Represents an error that can be displayed on a course section page.
    """

    class Place(Enum):
        CODE = 0
        COURSE = 1
        INSTRUCTOR = 2
        TAS = 3

    def __init__(self, msg: Union[PageError, str], place: Place):
        if type(msg) is str:
            self._msg = PageError(msg)
        elif type(msg) is PageError:
            self._msg = msg
        else:
            raise TypeError('Message must be a str or a PageError')

        self._place = place

    def error(self) -> PageError:
        return self._msg

    def place(self) -> Place:
        return self._place

    def place_code(self) -> bool:
        return self._place is SectionError.Place.CODE

    def place_course(self) -> bool:
        return self._place is SectionError.Place.COURSE

    def place_instructor(self) -> bool:
        return self._place is SectionError.Place.INSTRUCTOR

    def place_tas(self) -> bool:
        return self._place is SectionError.Place.TAS


class LabError:
    """
    Represents Errors than can be displayed on the lab section creation and editing pages.
    """

    class Place(Enum):
        CODE = 0
        SECTION = 1

    def __init__(self, msg: str, place: Place):
        self._msg = msg
        self._place = place

    def error(self) -> str:
        return self._msg

    def place(self) -> Place:
        return self._place

    def place_code(self) -> bool:
        return self._place is LabError.Place.CODE

    def place_section(self) -> bool:
        return self._place is LabError.Place.SECTION


class CourseError:
    class Place(Enum):
        CODE = 0
        NAME = 1

    def __init__(self, msg: str, place: Place):
        self._msg = msg
        self._place = place

    def error(self) -> str:
        return self._msg

    def place(self) -> Place:
        return self._place

    def place_code(self) -> bool:
        return self._place is CourseError.Place.CODE

    def place_name(self) -> bool:
        return self._place is CourseError.Place.NAME

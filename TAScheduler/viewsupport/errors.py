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


class UserEditPlace(Enum):
    USERNAME = 0
    PASSWORD = 1
    TYPE = 2
    PHONE = 3

    def username(self) -> bool:
        return self is UserEditPlace.USERNAME

    def password(self) -> bool:
        return self is UserEditPlace.PASSWORD

    def ty(self) -> bool:
        return self is UserEditPlace.TYPE

    def phone(self) -> bool:
        return self is UserEditPlace.PHONE


"""Represents errors that can be displayed on the user edit page"""
UserEditError = PageError[UserEditPlace]


class CourseEditPlace(Enum):
    CODE = 0
    NAME = 1

    def code(self) -> bool:
        return self is CourseEditPlace.CODE

    def name(self) -> bool:
        return self is CourseEditPlace.NAME


"""Represents errors which can be displayed on the course edit page"""
CourseEditError = PageError[CourseEditPlace]


class SectionEditPlace(Enum):
    CODE = 0
    COURSE = 1
    INSTRUCTOR = 2
    TAS = 3

    def code(self) -> bool:
        return self is SectionEditPlace.CODE

    def course(self) -> bool:
        return self is SectionEditPlace.COURSE

    def instructor(self) -> bool:
        return self is SectionEditPlace.INSTRUCTOR

    def tas(self) -> bool:
        return self is SectionEditPlace.TAS


"""Represents errors that can be displayed on the section edit page"""
SectionEditError = PageError[SectionEditPlace]


class LabEditPlace(Enum):
    CODE = 0
    SECTION = 1

    def code(self) -> bool:
        return self is LabEditPlace.CODE

    def section(self) -> bool:
        return self is LabEditPlace.SECTION


"""Represents errors which can be displayed on the lab edit page"""
LabEditError = PageError[LabEditPlace]


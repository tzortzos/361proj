from typing import Optional, Union
from enum import Enum, auto

class PageError:
    """
    Represents an error which may or may not have a headline, and which should be rendered with the
    `partials/inline_error.html` partial.
    """

    def __init__(self, body: str, headline: Optional[str] = None):
        """
        Create a new basic error with or without a headline value
        """
        self._body = body
        self._headline = headline

    def has_headline(self) -> bool:
        """
        Returns true if the error has a headline value, used by template
        to render as a error panel instead of alert.
        :return:
        """
        return self._headline is not None

    def headline(self) -> str:
        """
        Raises TypeError in the case that this error has no headline,
        use has_headline() to check beforehand.
        """

        if self._headline is None:
            raise TypeError('Tried to get headline from error without one')

        return self._headline

    def body(self) -> str:
        """
        Returns the body text of this error
        :return:
        """

        return self._body


class LoginError:
    """
    Represents an error to be used on the login page,
    placed with the username or password field depending on the variant
    """

    class Place(Enum):
        USERNAME = 0
        PASSWORD = 1

    def __init__(self, error_text: Union[PageError, str], place: Place):
        self._place = place
        if type(error_text) is PageError:
            self._error = error_text
        elif type(error_text) is str:
            self._error = PageError(error_text)
        else:
            raise TypeError('LoginError must be of type PageError or str')

    def error(self) -> PageError:
        """Gets the inner error of this instance of LoginError"""
        return self._error

    def place_username(self):
        """Returns true iff this login error is associated with the login field"""
        return self._place == LoginError.Place.USERNAME

    def place_password(self):
        """Returns true iff this login error is associated with the password field"""
        return self._place == LoginError.Place.PASSWORD


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


from typing import Optional, Union
from enum import Enum

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
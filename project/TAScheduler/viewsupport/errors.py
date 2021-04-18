from typing import Optional

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

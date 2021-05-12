from __future__ import annotations
from django.shortcuts import reverse
from TAScheduler.viewsupport.icons import IconItem
from TAScheduler.models import UserType
from typing import Union, Optional, Iterable, Callable
from enum import Enum


class NavbarItem:
    """
    Represents a single item in the application navbar. See templates/partials/sidebar.html for how it is used.
    """

    def __init__(self, name: str, url: str, enabled: bool = True, icon: Optional[Union[IconItem, str]] = None):
        self.name = name
        self.url = url
        self.enabled = enabled

        if icon is None:
            self.icon = None
        elif type(icon) is str:
            self.icon = IconItem(icon)
        elif type(icon) is IconItem:
            self.icon = icon
        else:
            raise TypeError('icon, if set, must be a str or an IconItem')

    def get_name(self) -> str:
        return self.name

    def get_url(self) -> str:
        return self.url

    def get_enabled(self) -> bool:
        return self.enabled

    def disable(self):
        """Do not enable this menu item"""
        self.enabled = False
        return self

    def has_icons(self):
        return self.icon is not None

    def get_icon_classes(self) -> Optional[str]:
        if self.icon is None:
            return None
        else:
            return self.icon.classes()


class AllItems(Enum):
    """Represents exactly one of the possible menu items for an admin,
    intended to be used as an iterable"""
    HOME =      [],                 NavbarItem('home', reverse('index'), icon='house-door-fill')
    MAIL =      [],                 NavbarItem('inbox', reverse('index'), icon='mailbox')
    USERS =     [],                 NavbarItem('user directory', reverse('users-directory'), icon='people-fill')
    COURSES =   [],                 NavbarItem('courses', reverse('courses-directory'), icon='text-paragraph')
    SECTIONS =  [],                 NavbarItem('course sections', reverse('sections-directory'), icon='kanban-fill')
    LABS =      [],                 NavbarItem('labs', reverse('labs-directory'), icon='bar-chart-fill')
    SKILLS =    [UserType.ADMIN],   NavbarItem('skills', reverse('skills-directory'), icon='award-fill')

    def __init__(self):
        self._for = None

    @classmethod
    def for_type(cls, user_type: UserType):
        """
        Create a new (partially applied) iterator to get the list of navbar items.

        can be used like:
        AllItems.for_type(UserType.ADMIN).without(AllItems.MAIL).iter()

        or
        AllItems.for_type(UserType.TA).iter()
        """

        class PartialIterator:
            """
            Represents a list of nav items for the current user
            has items which are not applicable to the current type removed
            has the option to select a current page
            """

            def __init__(self, partial):
                self._part = partial
                self._except = None

            @staticmethod
            def __map_disable__(maybe_disable: Optional[AllItems]) -> Callable[[AllItems], NavbarItem]:
                if maybe_disable is None:
                    return lambda a: a
                else:
                    def disable(item: AllItems) -> NavbarItem:
                        if maybe_disable == item:
                            item[1].disable()
                        return item[1]

                    return disable

            def without(self, item: AllItems) -> PartialIterator:
                """Disable the page item that you are currently on"""
                self._except = item
                return self

            def iter(self) -> Iterable[NavbarItem]:
                """Return the final iterable of items for the user type"""
                return map(PartialIterator.__map_disable__(self._except), self._part)

        # Return the partially applied iterator class defined above
        return PartialIterator(
            filter(
                lambda a: a[0] is [] or user_type in a[0],
                iter(cls),
            )
        )

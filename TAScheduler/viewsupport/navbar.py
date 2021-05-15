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
    HOME = 0
    MAIL = 1
    USERS = 2
    COURSES = 3
    SECTIONS = 4
    LABS = 5
    SKILLS = 6

    @classmethod
    def for_type(cls, user_type: Union[UserType, str]):
        """
        Create a new (partially applied) iterator to get the list of navbar items.

        can be used like:
        AllItems.for_type(UserType.ADMIN).without(AllItems.MAIL).iter()

        or
        AllItems.for_type(UserType.TA).iter()
        """

        if type(user_type) is str:
            user_type = UserType.from_str(user_type)

        items = {
            AllItems.HOME: ([], NavbarItem('home', reverse('index'), icon='house-door-fill')),
            AllItems.MAIL: ([], NavbarItem('inbox', reverse('index'), icon='mailbox')),  # TODO change me to final view name
            AllItems.USERS: ([], NavbarItem('user directory', reverse('users-directory'), icon='people-fill')),
            AllItems.COURSES: ([], NavbarItem('courses', reverse('courses-directory'), icon='text-paragraph')),
            AllItems.SECTIONS: ([], NavbarItem('course sections', reverse('sections-directory'), icon='kanban-fill')),
            AllItems.LABS: ([], NavbarItem('labs', reverse('labs-directory'), icon='bar-chart-fill')),
            AllItems.SKILLS: ([UserType.ADMIN], NavbarItem('skills', reverse('skills-directory'), icon='award-fill')),
        }

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
                    return lambda i: items[i][1]
                else:
                    def disable(i: AllItems) -> NavbarItem:
                        if maybe_disable == i:
                            items[i][1].disable()
                        return items[i][1]

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
                lambda a: items[a][0] == [] or user_type in items[a][0],
                iter(cls),
            )
        )

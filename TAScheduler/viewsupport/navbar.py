from django.shortcuts import reverse
from TAScheduler.viewsupport.icons import IconItem
from typing import Union, Optional, Iterable
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


class AdminItems(Enum):
    """Represents exactly one of the possible menu items for an admin,
    intended to be used as an iterable"""
    HOME = 0
    USERS = 1
    COURSES = 2
    SECTIONS = 3
    LABS = 4
    SKILLS = 5

    def get_item(self):
        if self == AdminItems.HOME:
            return NavbarItem('home', reverse('index'), icon='house-door-fill')
        elif self == AdminItems.USERS:
            return NavbarItem('user directory', reverse('users-directory'), icon='people-fill')
        elif self == AdminItems.COURSES:
            return NavbarItem('courses', reverse('courses-directory'), icon='text-paragraph')
        elif self == AdminItems.SECTIONS:
            return NavbarItem('course sections', reverse('sections-directory'), icon='kanban-fill')
        elif self == AdminItems.LABS:
            return NavbarItem('labs', reverse('labs-directory'), icon='bar-chart-fill')
        elif self == AdminItems.SKILLS:
            return NavbarItem('skills', reverse('skills-directory'), icon='award-fill')

    def map_disable(self):
        """
        returns a function to be used in map which will call get item for each
        AdminItem passed in, but disable in the case that that item is self
        """
        return lambda a : a.get_item() if a != self else a.get_item().disable()

    def items_iterable_except(self) -> Iterable[NavbarItem]:
        """
        Iterate over all AdminItems values, with the one equal to self disabled
        """
        return map(self.map_disable(), iter(AdminItems))

    @classmethod
    def items_iterable(cls) -> Iterable[NavbarItem]:
        """
        Iterate over all AdminItems values, with none disabled.
        """
        return map(lambda a: a.get_item(), iter(cls))


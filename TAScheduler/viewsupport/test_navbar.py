from django.test import TestCase
from TAScheduler.viewsupport.navbar import *


class TestNavbarItem(TestCase):
    def setUp(self):
        self.item_defaults = NavbarItem('home', '/home')
        self.item_not_enabled = NavbarItem('home', '/home', enabled=False)
        self.item_with_icon = NavbarItem('home', '/home', icon=IconItem('house'))

    def test_get_name(self):
        self.assertEqual(self.item_defaults.get_name(), 'home', 'name getter does not return value passed to init')

    def test_get_url(self):
        self.assertEqual(self.item_defaults.get_url(), '/home', 'url getter does not return value passed to init')

    def test_default_enabled(self):
        self.assertEqual(self.item_defaults.get_enabled(), True, 'items should be enabled by default')

    def test_default_no_icon(self):
        self.assertEqual(self.item_defaults.has_icons(), False, 'no icon was set so it should not say that it has an icon')
        self.assertIsNone(self.item_defaults.get_icon_classes(), 'no icon was set so should have defaulted to none')

    def test_constructor_disable(self):
        self.assertEqual(self.item_not_enabled.get_enabled(), False, 'init did not correctly disable item')

    def test_constructor_icon(self):
        self.assertEqual(type(self.item_with_icon.icon), IconItem, 'did not set correct inner type when setting icon in constructor')

    def test_gets_classes_with_icon(self):
        self.assertIsNotNone(self.item_with_icon.get_icon_classes(), 'get_icon_classes did not return inner icon.classes')

    def test_disable(self):
        self.item_defaults.disable()
        self.assertEqual(self.item_defaults.get_enabled(), False, 'call to disable did not disable item')

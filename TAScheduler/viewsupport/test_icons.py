import unittest
from TAScheduler.viewsupport.icons import *
from typing import Any

class TestIcons(unittest.TestCase):
    def test_inserts_name(self):
        icon = IconItem('home')
        self.assertEqual(icon.name, 'home', 'Did not insert string correctly')

    def test_returns_name(self):
        icon = IconItem('home')
        self.assertEqual(icon.take(), 'home', msg='Did not return correct member')

    def test_returns_classes(self):
        icon = IconItem('home')
        self.assertEqual(icon.classes(), 'glyphicon glyphicon-home')


if __name__ == '__main__':
    unittest.main()

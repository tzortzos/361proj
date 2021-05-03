from TAScheduler.models import UserType
from django.test import TestCase


class TestModels(TestCase):

    def setUp(self) -> None:
        self.maybe_type1 = 'A'
        self.maybe_type2 = ''
        self.maybe_type3 = 'Z'

    def test_from_str(self):
        response = UserType.from_str(self.maybe_type1)
        self.assertEqual(UserType.ADMIN, response, msg='Expected to ADMIN type returned.')

    def test_from_str_non_type(self):
        with self.assertRaises(TypeError):
            UserType.from_str(self.maybe_type3)

    def test_from_str_with_empty_maybe_type(self):
        with self.assertRaises(TypeError):
            UserType.from_str(self.maybe_type2)

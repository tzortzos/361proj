from django.test import TestCase
from TAScheduler.models import UserType
from TAScheduler.ClassDesign.Util import Util


class TestUtil(TestCase):

    def setUp(self) -> None:
        pass

    def test_optional_map_some(self):
        type_str = 'A'
        expected_type = UserType.ADMIN

        ty = Util[str, UserType].optional_map(
            UserType.try_from_str,
            type_str
        )

        self.assertIsNotNone(ty, 'Did not return some in optional map')
        self.assertEqual(expected_type, ty, 'Did not convert to correct type')

    def test_optional_map_none(self):
        type_str = None

        ty = Util[str, UserType].optional_map(
            UserType.try_from_str,
            type_str,
        )

        self.assertIsNone(ty, 'Did not return None as expected')

from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from django.test import TestCase


class TestUser(TestCase):

    def test_create_user(self):
        user_id = UserAPI.create_user(UserType.ADMIN, 'asmith', 'password123')
        self.assertTrue(user_id > 0, msg='Expecting id returned confirming saved to database.')



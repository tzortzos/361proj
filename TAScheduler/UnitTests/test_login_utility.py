import uuid
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from django.test import TestCase
from TAScheduler.models import User


class TestLoginUtility(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(type='A',univ_id=str(uuid.uuid4())[:6], password=str(uuid.uuid4())[:8])

    def test_update_password(self):
        new_pass = str(uuid.uuid4())[:8]
        LoginUtility.update_password(self.user1,new_pass)
        self.assertEqual(new_pass, self.user1.password, msg='Expected the password to have been updated.')
        self.assertEqual(False, self.user1.tmp_password, msg='Expected tmp password boolean to change to False.')


    def test_get_user_and_validate_by_user_id(self):
        new_pass = str(uuid.uuid4())[:8]
        LoginUtility.update_password(self.user1,new_pass)
        user = LoginUtility.get_user_and_validate_by_user_id(self.user1.user_id)
        self.assertEqual(self.user1, user, msg='Expected user to be returned because exists and tmp password false')

    def test_get_user_and_validate_by_user_with_edit_redirect(self):
        user = LoginUtility.get_user_and_validate_by_user_id(self.user1.user_id)
        self.assertEqual('/user-edit/', user.url, msg='Expected redirect to password updated page.')

    def test_get_user_and_validate_by_user_login_redirect(self):
        user = LoginUtility.get_user_and_validate_by_user_id(0)
        self.assertEqual('/login/', user.url, msg='Expected redirect to login for non-existent user.')

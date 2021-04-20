from django.test import Client, TestCase
from TAScheduler.models import User, UserType


class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.check_pass = 'password1'
        long_user = User.objects.create(
            type=UserType.ADMIN,
            univ_id='josiahth',
            password=self.check_pass,
            l_name='hilden',
            f_name='josiah',
            tmp_password=False
        )

        self.long_user = long_user.user_id

        short_user = User.objects.create(
            type=UserType.PROF,
            univ_id='nleverence',
            password=self.check_pass,
        )

        self.short_user = short_user

    def test_rejects_empty_username(self):
        pass

    def test_rejects_long_username(self):
        # Usernames may not be longer than 20 characters,
        # does not even ask the database
        pass

    def test_rejects_no_such_username(self):
        # Username does not exist in the database
        pass

    def test_rejects_empty_password(self):
        pass

    def test_rejects_short_password(self):
        # Passwords of less than or equal to 8 passwords are not valid
        pass

    def test_rejects_mismatched_password(self):
        # Username and password do not match
        pass

    def test_successful_login_sets_session(self):
        # Successful login sets the session with the users' primary key (user_id)
        # from the database
        pass

    def test_successful_login_sends_redirect(self):
        # Successful login redirects the user to their homepage
        pass

    def test_first_login_sends_redirect(self):
        # Successful login, when a user has not logged in before,
        # redirects them to the password change form
        pass

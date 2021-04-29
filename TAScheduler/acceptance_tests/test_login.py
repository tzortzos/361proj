from django.test import Client, TestCase
from TAScheduler.models import User, UserType
from django.urls import reverse
from TAScheduler.viewsupport.errors import PageError, LoginError


class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.check_pass = 'password1'

        self.long_user_username = 'josiahth'
        long_user = User.objects.create(
            type=UserType.ADMIN,
            univ_id=self.long_user_username,
            password=self.check_pass,
            l_name='hilden',
            f_name='josiah',
            tmp_password=False
        )

        self.long_user = long_user.id

        self.short_user_username = 'nleverence'
        short_user = User.objects.create(
            type=UserType.PROF,
            univ_id=self.short_user_username,
            password=self.check_pass,
        )

        self.short_user = short_user

    def test_rejects_empty_username(self):
        resp = self.client.post(reverse('login'), {
            'username': '',
            'password': 'verysecurepassword'
        })

        error: LoginError= resp.context['error']

        self.assertIsNotNone(error, 'Did not return error message')
        self.assertTrue(error.place_username(), 'Did not return error with username')
        self.assertEqual(error.error().body(), 'You must provide a username')

    def test_rejects_long_username(self):
        # Usernames may not be longer than 20 characters,
        # does not even ask the database

        resp = self.client.post(reverse('login'), {
            'username': 'very_long_username_username_that_the_database_cannot_hold',
            'password': 'verysecurepassword',
        })

        error: LoginError = resp.context['error']

        self.assertIsNotNone(error, 'Did not return error for too long username')
        self.assertTrue(error.place_username(), 'Did not return error for username')
        self.assertEqual(error.error().body(), 'That Username is too Long')

    def test_rejects_no_such_username(self):
        # Username does not exist in the database
        resp = self.client.post(reverse('login'), {
            'username': 'jschiltz19',
            'password': 'password1',
        })

        error = resp.context['error']

        self.assertIsNotNone(error, 'Did not return error for nonexistent user')
        self.assertTrue(error.place_username(), 'Did not return error for non-existence username.')
        self.assertEqual(error.error().body(), 'No such user')

    def test_rejects_empty_password(self):
        resp = self.client.post(reverse('login'), {
            'username': self.long_user_username,
            'password': ''
        })

        error: LoginError = resp.context['error']

        self.assertIsNotNone(error, 'Did not return error message')
        self.assertTrue(error.place_password(), 'Did not return error with password')
        self.assertEqual(error.error().body(), 'You must provide a password')

    def test_rejects_short_password(self):
        # Passwords of less than or equal to 8 passwords are not valid
        resp = self.client.post(reverse('login'), {
            'username': self.long_user_username,
            'password': '1234'
        })

        error: LoginError = resp.context['error']

        self.assertIsNotNone(error, 'Did not return error message')
        self.assertTrue(error.place_password(), 'Did not return error with password')
        self.assertEqual(error.error().body(), 'A password must be at least 8 characters in length')

    def test_rejects_mismatched_password(self):
        # Username and password do not match
        resp = self.client.post(reverse('login'), {
            'username': self.long_user_username,
            'password': '1234567890'
        })

        error: LoginError = resp.context['error']

        self.assertIsNotNone(error, 'Did not return error message')
        self.assertTrue(error.place_password(), 'Did not return error with password')
        self.assertEqual(error.error().body(), 'Incorrect Password')

    def test_successful_login_sets_session(self):
        # Successful login sets the session with the users' primary key (user_id)
        # from the database
        resp = self.client.post(reverse('login'), {
            'username': self.long_user_username,
            'password': self.check_pass,
        })

        try:
            user_id = self.client.session['user_id']
        except KeyError:
            self.assertTrue(False, 'Did not set user_id on successful login')

        self.assertIsNotNone(user_id, 'Did not set user_id on login')
        self.assertEqual(user_id, self.long_user, 'Did not set correct key with valid login')

    def test_successful_login_sends_redirect(self):
        # Successful login redirects the user to their homepage
        resp = self.client.post(reverse('login'), {
            'username': self.long_user_username,
            'password': self.check_pass,
        }, follow=True)

        redirects = resp.redirect_chain

        self.assertEqual(len(redirects), 1, 'Redirected too many times')
        self.assertEqual(redirects[0][0], reverse('index'), 'Did not redirect returning user to homepage')

    def test_first_login_sends_redirect(self):
        # Successful login, when a user has not logged in before,
        # redirects them to the password change form
        resp = self.client.post(reverse('login'), {
            'username': self.short_user_username,
            'password': self.check_pass,
        }, follow=True)

        self.assertRedirects(resp, reverse('users-edit', args=(self.short_user.id,)))

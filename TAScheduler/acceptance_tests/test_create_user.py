from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType
from TAScheduler.viewsupport.errors import PageError, UserEditError


class TestCreateUserView(TestCase):
    def setUp(self):
        self.client = Client()

        # Only admins may create new users, so we need the
        # session to have one for most tests

        self.admin_username = 'josiahth'
        self.admin = User.objects.create(univ_id=self.admin_username,
                                         password='a-very-good-password',
                                         type=UserType.ADMIN,
                                         tmp_password=False)

        self.client.session['user_id'] = self.admin.user_id

        self.prof_username = 'jrock'
        self.professor = User.objects.create(univ_id=self.prof_username,
                                             password='a-very-goog-password',
                                             type=UserType.PROF,
                                             tmp_password=False)

    def get_error(self, resp) -> UserEditError:
        resp_context = resp.context

        self.assertIsNotNone(resp_context['error'], 'Did not return error in context on empty password')
        self.assertEqual(type(resp_context['error']), UserEditError, 'Did not return correctly typed error')

        return resp_context['error']

    def test_rejects_empty_password(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            # 'new_password': '',
            'user_type': 'T',

        }, follow=True)

        self.assertIsNotNone(resp, 'Did not return a response')
        self.assertEqual(len(resp.redirect_chain), 0, 'Should not redirect on failed insertion')

        ret_error = self.get_error(resp)

        self.assertTrue(ret_error.place() is UserEditError.Place.PASSWORD, 'Did not recognize that password was empty')
        self.assertEqual(ret_error.error().body(), 'Password must be at least 8 characters in length')

    def test_rejects_short_password(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': '1234567',  # Short password
            'user_type': 'T',

        }, follow=True)

        self.assertIsNotNone(resp, 'Did not return a response')
        self.assertEqual(len(resp.redirect_chain), 0, 'Should not redirect on failed insertion')

        ret_error = self.get_error(resp)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.PASSWORD, 'Did not recognize that password was empty')
        self.assertEqual(ret_error.error().body(), 'Password must be at least 8 characters in length')

    def test_rejects_empty_username(self):
        resp = self.client.post(reverse('users-create'), {
            # 'univ_id': '',
            'new_password': 'a-very-good-password',  # Short password
            'user_type': 'T',

        }, follow=True)

        self.assertIsNotNone(resp, 'Did not return a response')
        self.assertEqual(len(resp.redirect_chain), 0, 'Should not redirect on failed insertion')

        ret_error = self.get_error(resp)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'You must provide a university id')

    def test_rejects_long_username(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'a-very-long-username-that-would-never-fit-in-the-database',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=True)

        self.assertIsNotNone(resp, 'Did not return a response')
        self.assertEqual(len(resp.redirect_chain), 0, 'Should not redirect on failed insertion')

        ret_error = self.get_error(resp)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'The username may not be longer than 20 characters')

    def test_rejects_username_with_at_sign(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'areasonableusername@uwm.edu',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=True)

        self.assertIsNotNone(resp, 'Did not return a response')
        self.assertEqual(len(resp.redirect_chain), 0, 'Should not redirect on failed insertion')

        ret_error = self.get_error(resp)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'You only need to put in the first part of a university email')

    def test_rejects_username_with_spaces(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'areasonableusername uwm edu',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=True)

        self.assertIsNotNone(resp, 'Did not return a response')
        self.assertEqual(len(resp.redirect_chain), 0, 'Should not redirect on failed insertion')

        ret_error = self.get_error(resp)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'A username may not have spaces')

    def test_rejects_non_admin(self):
        self.client.session['user_id'] = self.professor.user_id
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=True)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(univ_id='nleverence')

        redirects = resp.redirect_chain

        self.assertEqual(len(redirects), 1, 'Redirected the wrong number of times')
        self.assertEqual(
            redirects[0][0],
            reverse('user-directory'),
            'Did not redirect user to user directory in the case that they were not allowed to create users'
        )

    def test_rejects_missing_session(self):
        del self.client.session['user_id']
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=True)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(univ_id='nleverence')

        redirects = resp.redirect_chain

        self.assertEqual(len(redirects), 1, 'Redirected the wrong number of times')
        self.assertEqual(
            redirects[0][0],
            reverse('index'),
            'Did not redirect user to user directory in the case that they were not allowed to create users'
        )
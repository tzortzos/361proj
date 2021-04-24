from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType
from TAScheduler.viewsupport.errors import PageError, UserEditError


class TestCreateUserView(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        # Only admins may create new users, so we need the
        # session to have one for most tests

        self.admin_username = 'josiahth'
        self.admin = User.objects.create(univ_id=self.admin_username,
                                         password='a-very-good-password',
                                         type=UserType.ADMIN,
                                         tmp_password=False)

        self.session['user_id'] = self.admin.user_id
        self.session.save()

        self.prof_username = 'jrock'
        self.professor = User.objects.create(univ_id=self.prof_username,
                                             password='a-very-goog-password',
                                             type=UserType.PROF,
                                             tmp_password=False)

    def get_error(self, resp_context) -> UserEditError:
        self.assertIsNotNone(resp_context['error'], 'Did not return error in context on empty password')
        self.assertEqual(type(resp_context['error']), UserEditError, 'Did not return correctly typed error')

        return resp_context['error']

    def test_rejects_empty_password(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            # 'new_password': '',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        ret_error = self.get_error(resp.context)

        self.assertTrue(ret_error.place() is UserEditError.Place.PASSWORD, 'Did not recognize that password was empty')
        self.assertEqual(ret_error.error().body(), 'Password must be at least 8 characters in length')

    def test_rejects_short_password(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': '1234567',  # Short password
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        ret_error = self.get_error(resp.context)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.PASSWORD, 'Did not recognize that password was empty')
        self.assertEqual(ret_error.error().body(), 'Password must be at least 8 characters in length')

    def test_rejects_empty_username(self):
        resp = self.client.post(reverse('users-create'), {
            # 'univ_id': '',
            'new_password': 'a-very-good-password',  # Short password
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        ret_error = self.get_error(resp.context)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'You must provide a university id')

    def test_rejects_long_username(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'a-very-long-username-that-would-never-fit-in-the-database',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        ret_error = self.get_error(resp.context)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'A university id may not be longer than 20 characters')

    def test_rejects_username_with_at_sign(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'areasoname@uwm.edu',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        ret_error = self.get_error(resp.context)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'You only need to put in the first part of a university email')

    def test_rejects_username_with_spaces(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'ame uwm edu',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        ret_error = self.get_error(resp.context)  # Asserts that an error exists as well

        self.assertTrue(ret_error.place() is UserEditError.Place.USERNAME, 'Did not recognize missing username')
        self.assertEqual(ret_error.error().body(), 'A username may not have spaces')

    def test_rejects_non_admin(self):
        self.client.session['user_id'] = self.professor.user_id
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        old_user = User.objects.get(univ_id='nleverence')
        self.assertIsNotNone(old_user, 'Did not remove user')

        self.assertRedirects(resp, reverse('users-directory'))

    def test_rejects_missing_session(self):
        del self.session['user_id']
        self.session.save()
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(univ_id='nleverence')

        self.assertRedirects(resp, reverse('login'))

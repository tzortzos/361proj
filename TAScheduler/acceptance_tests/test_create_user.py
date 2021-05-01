from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType
from TAScheduler.viewsupport.errors import UserEditPlace, UserEditError
from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.message import MessageQueue, Message

class TestCreateUserView(TASAcceptanceTestCase[UserEditError]):
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

        self.session['user_id'] = self.admin.id
        self.session.save()

        self.prof_username = 'jrock'
        self.professor = User.objects.create(univ_id=self.prof_username,
                                             password='a-very-goog-password',
                                             type=UserType.PROF,
                                             tmp_password=False)

    def test_rejects_empty_password(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            # 'new_password': '',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        error = self.assertContextError(resp)

        self.assertTrue(error.place() is UserEditPlace.PASSWORD)
        self.assertEqual('Password must be at least 8 characters in length', error.message())

    def test_rejects_short_password(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': '1234567',  # Short password
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        error = self.assertContextError(resp)  # Asserts that an error exists as well

        self.assertTrue(error.place() is UserEditPlace.PASSWORD)
        self.assertEqual('Password must be at least 8 characters in length', error.message())

    def test_rejects_empty_username(self):
        resp = self.client.post(reverse('users-create'), {
            # 'univ_id': '',
            'new_password': 'a-very-good-password',  # Short password
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        error = self.assertContextError(resp)  # Asserts that an error exists as well

        self.assertTrue(error.place() is UserEditPlace.USERNAME)
        self.assertEqual('You must provide a university id', error.message())

    def test_rejects_long_username(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'a-very-long-username-that-would-never-fit-in-the-database',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        error = self.assertContextError(resp)  # Asserts that an error exists as well

        self.assertTrue(error.place() is UserEditPlace.USERNAME, 'Did not recognize missing username')
        self.assertEqual('A university id may not be longer than 20 characters', error.message())

    def test_rejects_username_with_at_sign(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'areasoname@uwm.edu',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        error = self.assertContextError(resp)  # Asserts that an error exists as well

        self.assertTrue(error.place() is UserEditPlace.USERNAME, 'Did not recognize missing username')
        self.assertEqual('You only need to put in the first part of a university email', error.message())

    def test_rejects_username_with_spaces(self):
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'ame uwm edu',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response')

        error = self.assertContextError(resp)  # Asserts that an error exists as well

        self.assertTrue(error.place() is UserEditPlace.USERNAME, 'Did not recognize missing username')
        self.assertEqual('A username may not have spaces', error.message())

    def test_rejects_non_admin(self):
        self.client.session['user_id'] = self.professor.id
        resp = self.client.post(reverse('users-create'), {
            'univ_id': 'nleverence',
            'new_password': 'a-very-good-password',
            'user_type': 'T',

        }, follow=False)

        self.assertContainsMessage(resp,
                                   Message('You do not have permission to create users', Message.Type.ERROR))

        old_user = User.objects.get(username='nleverence')
        self.assertIsNotNone(old_user, 'Did not remove user')

        self.assertRedirects(resp, reverse('users-directory'))


from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse

from TAScheduler.models import User, UserType


class TestCreateUserView(TestCase):
    def setUp(self):
        self.client = Client()

        # Only admins may create new users, so we need the
        # session to have one for most tests

        self.admin_username = 'josiahth'
        self.admin = User.objects.create(univ_id=self.admin_username, password='a-very-good-password', type=UserType.ADMIN)
        self.client.session['user_id'] = self.admin.user_id

    def test_rejects_empty_password(self):
        resp = self.client.post(reversed('create-user'), {
            'univ_id': 'nathanl',
            'password': '',
            'user_type': 'T',

        }, follow=True)

        self.assertIsNotNone(resp, 'Did not return a response')
        self.assertEqual(len(resp.redirect_chain), 0, 'Should not redirect on failed insertion')

        resp_context = resp.context

        self.assertIsNotNone(resp_context['error'], 'Did not return error in context on empty password')
        self.assertEqual(type(resp_context['error']))

    def test_rejects_short_password(self):
        pass

    def test_rejects_empty_username(self):
        pass

    def test_rejects_long_username(self):
        pass

    def test_rejects_username_with_special_characters(self):
        pass

    def test_rejects_non_admin(self):
        pass

    def test_rejects_missing_session(self):
        pass
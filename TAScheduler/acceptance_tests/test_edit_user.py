from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType
from TAScheduler.viewsupport.errors import UserEditError, PageError


class TestEditUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.old_password = 'a-very-good-password'

        self.admin_username = 'josiahth'
        self.admin = User.objects.create(
            univ_id=self.admin_username,
            password=self.old_password,
            tmp_password=False,
            type=UserType.ADMIN
        )

        self.admin_edit_url = reverse('users-edit', self.admin.user_id)

        self.prof_username = 'nleverence'
        self.prof = User.objects.create(
            univ_id=self.prof_username,
            password=self.old_password,
            tmp_password=False,
            type=UserType.PROF
        )

        self.prof_edit_url = reverse('users-edit', self.prof.user_id)

        self.client.session['user_id'] = self.admin.user_id

    def set_admin_session(self):
        self.client.session['user_id'] = self.admin.user_id

    def set_prof_session(self):
        self.client.session['user_id'] = self.prof.user_id

    def assertUserEditError(self, resp: HttpResponse) -> UserEditError:
        """Assert that a UserEditError was returned in the context and return it"""
        context = resp.context

        self.assertIsNotNone(context['error'], 'Did not return error')
        self.assertEqual(type(context['error']), UserEditError, 'Did not return correctly typed error')

        return context['error']

    def test_edit_self_contact(self):
        pass

    def test_edit_self_password(self):
        pass

    def test_edit_self_updates_database(self):
        pass

    def test_admin_edit_other_updates_database(self):
        pass

    def test_rejects_admin_edit_other_password(self):
        pass

    def test_admin_edit_other_type(self):
        pass

    def test_admin_edit_other_contact(self):
        pass

    def test_rejects_empty_username(self):
        pass

    def test_rejects_too_long_username(self):
        pass

    def test_rejects_incorrect_password_change(self):
        pass

    def test_rejects_empty_password_change(self):
        pass

    def test_rejects_too_short_password_change(self):
        pass

    def test_rejects_invalid_phone(self):
        pass

    def test_rejects_non_admin_edit_other(self):
        pass

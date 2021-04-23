from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist
from typing import Optional

from TAScheduler.models import User, UserType
from TAScheduler.viewsupport.errors import UserEditError, PageError
from TAScheduler.viewsupport.message import Message, MessageQueue


class TestEditUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.old_password = 'a-very-good-password'
        self.new_password = 'another-lesser-password'
        self.new_phone = '2622915566'

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

    def set_admin_session(self):
        self.client.session['user_id'] = self.admin.user_id

    def set_prof_session(self):
        self.client.session['user_id'] = self.prof.user_id

    def assertDoesNotRedirect(self, resp, msg: Optional[str] = None):
        if msg is None:
            msg = f'Page redirected with sequence {resp.redirect_chain}'

        self.assertEqual(len(resp.redirect_chain), 0, msg)

    def get_message(self, resp, nth: int = 0) -> Message:
        self.assertIsNotNone(resp.context['messages'], 'Did not send success message to user')
        self.assertTrue(len(resp.context['messages']) == 1, 'Did not send any success messages to user')

        return resp.context['messages'][nth]

    def assertContainsMessage(self, resp, message: Message, msg: str = 'Message object was not in context'):
        self.assertTrue(message in MessageQueue.get(resp.client.session), msg=msg)

    def assertUserEditError(self, resp) -> UserEditError:
        """Assert that a UserEditError was returned in the context and return it"""
        context = resp.context

        self.assertIsNotNone(context['error'], 'Did not return error')
        self.assertEqual(type(context['error']), UserEditError, 'Did not return correctly typed error')

        return context['error']

    def test_edit_self_contact(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'username': self.admin_username,
            'phone': '4253084859'
        }, follow=True)

        self.assertRedirects(
            reverse('users-view', self.admin.user_id),
            'Did not redirect to user view page on successful edit'
        )

        self.assertContainsMessage(resp, Message('Contact Information Updated'))

    def test_edit_self_password(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'username': self.admin_username,
            'old_password': self.old_password,
            'new_password': self.new_password,
        }, follow=True)

        self.assertRedirects(
            reverse('users-view', self.admin.user_id),
            'Did not redirect to user view page on successful edit'
        )

        self.assertContainsMessage(resp, Message('Password Updated'))

    def test_edit_self_updates_database(self):
        # This test uses the professor to update self instead of admin, to cover more use cases
        self.set_prof_session()
        resp = self.client.post(self.prof_edit_url, {
            'username': self.prof_username,
            'phone': self.new_phone,
        }, follow=True)

        new_prof = User.objects.get(univ_id=self.prof_username)

        self.assertIsNotNone(new_prof)
        self.assertEqual(new_prof.phone, self.new_phone, 'Did not change contact information in database')

    def test_admin_edit_other_updates_database(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'username': self.prof_username,
            'phone': self.new_phone,
        }, follow=True)

        new_prof = User.objects.get(univ_id=self.prof_username)

        self.assertIsNotNone(new_prof)
        self.assertEqual(new_prof.phone, self.new_phone, 'Did not change contact information in database')

    def test_rejects_admin_edit_other_password(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'username': self.prof_username,
            'old_password': self.old_password,
            'new_password': self.new_password,
        }, follow=True)

        self.assertDoesNotRedirect(resp, 'Tried to redirect after failing to update user')

        self.assertContainsMessage(resp, Message('You may not change another users password', Message.Type.ERROR))

    def test_admin_edit_other_type(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'username': self.prof_username,
            'user_type': 'A'
        }, follow=True)

        self.assertRedirects(
            reverse('users-view', self.prof.user_id),
            'Did not redirect to user info screen after changing user type'
        )

        self.assertContainsMessage(
            resp,
            Message(f'User {self.prof.univ_id} is now a Administrator')
        )

    def test_rejects_empty_username(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'username': ''

        }, follow=True)

        self.assertDoesNotRedirect()

        error = self.assertUserEditError(resp)
        self.assertTrue(error.place() is UserEditError.Place.USERNAME,
                        msg='Didn\'t return username error when attempting to remove username.')
        self.assertEqual(error.error().body(), 'You can\'t remove a user\'s username.')

    def test_rejects_too_long_username(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'username': 'a-very-long-username-that-the-database-could-not-hold'

        }, follow=True)

        self.assertDoesNotRedirect()

        error = self.assertUserEditError(resp)
        self.assertTrue(error.place() is UserEditError.Place.USERNAME,
                        msg='Should have received an error about an username that was too long.')
        self.assertEqual(error.error().body(), 'A username may not be longer than 20 characters.')


    def test_rejects_incorrect_password_change(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'username': self.admin_username,
            'old_password': 'a password that is definitely correct',
            'new_password': self.new_password,
        }, follow=True)

        self.assertDoesNotRedirect()

        error = self.assertUserEditError(resp)
        self.assertTrue(error.place() is UserEditError.Place.PASSWORD,
                    msg='Should have received an error about incorrect password.')
        self.assertEqual(error.error().body(), 'Incorrect password')



    def test_rejects_empty_password_change(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'username': self.admin_username,
            'old_password': self.old_password,
            'new_password': '',
        }, follow=True)

        self.assertDoesNotRedirect()

        error = self.assertUserEditError(resp)
        self.assertTrue(error.place() is UserEditError.Place.PASSWORD,
                        msg='Should have recieved an error about empty new password.')
        self.assertEqual(error.error().body(), 'New Password can\'t be empty.')


    def test_rejects_too_short_password_change(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'username': self.admin_username,
            'old_password': self.old_password,
            'new_password': '1234',
        }, follow=True)

        self.assertDoesNotRedirect()

        error = self.assertUserEditError(resp)
        self.assertTrue(error.place() is UserEditError.Place.PASSWORD,
                        msg='Should have received an error about new password being too short.')
        self.assertEqual(error.error().body(), 'New Password needs to be 8 or more characters.')

    def test_rejects_invalid_phone(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'username': self.admin_username,
            'phone': '123456'
        }, follow=True)

        self.assertDoesNotRedirect()

        error = self.assertUserEditError(resp)
        self.assertTrue(error.place() is UserEditError.Place.PHONE,
                        msg='Should have received an error about incorrect phone edit.')
        self.assertEqual(error.error().body(), 'Phone number needs to be exactly 10 digits long.')

    def test_rejects_non_admin_edit_other(self):
        self.set_prof_session()
        resp_post = self.client.post(self.admin_edit_url, {
            'username': self.admin_username,
            'phone': '123456'
        }, follow=True)

        self.assertRedirects(reverse('index'))

        self.assertContainsMessage(resp_post, Message('You are not allowed to edit other users.', Message.Type.ERROR))

        resp_get = self.client.get(self.admin_edit_url, {}, follow=True)

        self.assertRedirects(reverse('index'))

        self.assertContainsMessage(resp_get, Message('You are not allowed to edit other users.', Message.Type.ERROR))

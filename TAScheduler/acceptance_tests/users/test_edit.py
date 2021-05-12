from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist
from typing import Optional

from TAScheduler.models import User, UserType
from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import UserEditError, UserEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue


class TestEditUser(TASAcceptanceTestCase[UserEditError]):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        self.old_password = 'a-very-good-password'
        self.new_password = 'another-lesser-password'
        self.new_phone = '2622915566'

        self.admin_username = 'josiahth'
        self.admin = User.objects.create(
            username=self.admin_username,
            password=self.old_password,
            password_tmp=False,
            type=UserType.ADMIN
        )

        self.admin_edit_url = reverse('users-edit', args=(self.admin.id,))

        self.prof_username = 'nleverence'
        self.prof = User.objects.create(
            username=self.prof_username,
            password=self.old_password,
            password_tmp=False,
            type=UserType.PROF
        )

        self.prof_edit_url = reverse('users-edit', args=(self.prof.id,))

    def set_admin_session(self):
        self.session['user_id'] = self.admin.id
        self.session.save()

    def set_prof_session(self):
        self.session['user_id'] = self.prof.id
        self.session.save()

    def test_edit_self_contact(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'univ_id': self.admin_username,
            'phone': '4253084859'
        }, follow=False)

        self.assertContainsMessage(resp, Message('Contact Information Updated'))

        self.assertRedirects(
            resp,
            reverse('users-view', args=(self.admin.id,))
        )

    def test_edit_self_password(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'univ_id': self.admin_username,
            'old_password': self.old_password,
            'new_password': self.new_password,
        }, follow=False)

        self.assertContainsMessage(resp, Message('Password Updated'))

        self.assertRedirects(
            resp,
            reverse('users-view', args=(self.admin.id,)),
        )


    def test_edit_self_updates_database(self):
        # This test uses the professor to update self instead of admin, to cover more use cases
        self.set_prof_session()
        resp = self.client.post(self.prof_edit_url, {
            'univ_id': self.prof_username,
            'phone': self.new_phone,
        }, follow=False)

        new_prof = User.objects.get(username=self.prof_username)

        self.assertIsNotNone(new_prof)
        self.assertEqual(new_prof.phone, self.new_phone, 'Did not change contact information in database')

    def test_admin_edit_other_updates_database(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'univ_id': self.prof_username,
            'phone': self.new_phone,
        }, follow=False)

        new_prof = User.objects.get(username=self.prof_username)

        self.assertIsNotNone(new_prof)
        self.assertEqual(new_prof.phone, self.new_phone, 'Did not change contact information in database')

    def test_rejects_admin_edit_other_password(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'univ_id': self.prof_username,
            'old_password': self.old_password,
            'new_password': self.new_password,
        }, follow=False)

        self.assertContainsMessage(resp, Message('You may not change another users password', Message.Type.ERROR))

        # self.assertDoesNotRedirect(resp, 'Tried to redirect after failing to update user')

    def test_admin_edit_other_type(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'univ_id': self.prof_username,
            'user_type': 'A'
        }, follow=False)

        self.assertContainsMessage(
            resp,
            Message(f'User {self.prof.username} is now a Administrator')
        )

        self.assertRedirects(resp, reverse('users-view', args=(self.prof.id,)))

    def test_rejects_empty_username(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'univ_id': ''

        }, follow=True)

        error = self.assertContextError(resp)

        self.assertTrue(error.place() is UserEditPlace.USERNAME,
                        msg='Didn\'t return username error when attempting to remove username.')
        self.assertEqual(error.message(), 'You can\'t remove a user\'s username.')

    def test_rejects_too_long_username(self):
        self.set_admin_session()
        resp = self.client.post(self.prof_edit_url, {
            'univ_id': 'a-very-long-username-that-the-database-could-not-hold'

        }, follow=True)

        error = self.assertContextError(resp)
        self.assertTrue(error.place() is UserEditPlace.USERNAME,
                        msg='Should have received an error about an username that was too long.')
        self.assertEqual(error.message(), 'A username may not be longer than 20 characters.')

    def test_rejects_incorrect_password_change(self):
        self.session['user_id'] = self.admin.id
        self.session.save()

        resp = self.client.post(self.admin_edit_url, {
            'univ_id': self.admin_username,
            'old_password': 'a password that is definitely correct',
            'new_password': self.new_password,
        }, follow=True)

        error = self.assertContextError(resp)
        self.assertTrue(error.place() is UserEditPlace.PASSWORD,
                    msg='Should have received an error about incorrect password.')
        self.assertEqual(error.message(), 'Incorrect password')



    def test_rejects_empty_password_change(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'univ_id': self.admin_username,
            'old_password': self.old_password,
            'new_password': '',
        }, follow=True)

        error = self.assertContextError(resp)
        self.assertTrue(error.place() is UserEditPlace.PASSWORD,
                        msg='Should have recieved an error about empty new password.')
        self.assertEqual(error.message(), 'New password can\'t be empty.')


    def test_rejects_too_short_password_change(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'univ_id': self.admin_username,
            'old_password': self.old_password,
            'new_password': '1234',
        }, follow=True)

        error = self.assertContextError(resp)
        self.assertTrue(error.place() is UserEditPlace.PASSWORD,
                        msg='Should have received an error about new password being too short.')
        self.assertEqual(error.message(), 'New Password needs to be 8 or more characters.')

    def test_rejects_invalid_phone(self):
        self.set_admin_session()
        resp = self.client.post(self.admin_edit_url, {
            'univ_id': self.admin_username,
            'phone': '123456'
        }, follow=True)

        error = self.assertContextError(resp)

        self.assertTrue(error.place() is UserEditPlace.PHONE,
                        msg='Should have received an error about incorrect phone edit.')
        self.assertEqual(error.message(), 'Phone number needs to be exactly 10 digits long.')

    def test_rejects_non_admin_edit_other(self):
        self.set_prof_session()
        resp_post = self.client.post(self.admin_edit_url, {
            'univ_id': self.admin_username,
            'phone': '123456'
        }, follow=False)

        self.assertContainsMessage(resp_post, Message('You are not allowed to edit other users.', Message.Type.ERROR))

        self.assertRedirects(resp_post, reverse('index'))

        resp_get = self.client.get(self.admin_edit_url, {}, follow=False)

        self.assertContainsMessage(resp_get, Message('You are not allowed to edit other users.', Message.Type.ERROR))

        self.assertRedirects(resp_get, reverse('index'))

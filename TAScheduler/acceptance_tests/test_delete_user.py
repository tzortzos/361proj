from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist
from django.contrib.sessions.backends.base import SessionBase

from typing import List

from TAScheduler.models import User, UserType
from TAScheduler.viewsupport.message import Message, MessageQueue


class TestDeleteUser(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_username = 'josiahth'
        self.admin = User.objects.create(
            univ_id=self.admin_username,
            password='a-very-good-password',
            tmp_password=False,
            type=UserType.ADMIN
        )

        self.prof_username = 'nleverence'
        self.prof = User.objects.create(
            univ_id=self.prof_username,
            password='a-very-good-password',
            tmp_password=False,
            type=UserType.PROF
        )

        self.valid_delete_url = reverse('users-delete', args=(self.prof.user_id,))
        self.valid_delete_self = reverse('users-delete', args=(self.admin.user_id,))
        self.invalid_delete_url = reverse('users-delete', args=(340000,))  # Only two users were created so the max valid id is 2

        self.session = self.client.session
        self.session['user_id'] = self.admin.user_id
        self.session.save()


    def get_first_message(self, resp) -> Message:
        session = resp.client.session
        self.assertTrue('messages' in session, msg='Session does not contain any message')
        try:
            messages = MessageQueue.get(session)
            return messages[0]
        except KeyError:
            self.assertTrue(False, 'Session does not contain any messages')

    def test_admin_can_delete_existing(self):
        resp = self.client.post(self.valid_delete_url, {})

        message: Message = self.get_first_message(resp)

        self.assertIsNotNone(resp, 'Post did not return value')
        self.assertRedirects(resp, reverse('users-directory'))

        self.assertTrue(message.type() is Message.Type.REGULAR, 'Did not send correct message type')
        self.assertEqual(message.message(), f'Successfully deleted user {self.prof_username}', 'Did not return correct message')

    def test_delete_nonexistent_redirects_with_error(self):
        resp = self.client.post(self.invalid_delete_url, {}, follow=False)

        message: Message = self.get_first_message(resp)

        self.assertIsNotNone(resp, 'Post did not return value')
        self.assertRedirects(resp, reverse('users-directory'))

        self.assertTrue(message.type() is Message.Type.ERROR, 'Did not send correct message type')
        self.assertEqual(message.message(), f'No user with id {340000} exists', 'Did not return correct message')

    def test_prof_cannot_delete_anyone(self):
        self.session['user_id'] = self.prof.user_id
        self.session.save()

        resp_post = self.client.post(reverse('users-delete', args=(self.admin.user_id,)), {}, follow=False)
        resp_get = self.client.get(reverse('users-delete', args=(self.admin.user_id,)), {}, follow=False)

        message_post = self.get_first_message(resp_post)
        message_get = self.get_first_message(resp_get)

        self.assertIsNotNone(resp_post, 'Post did not return value')
        self.assertIsNotNone(resp_get, 'Get did not return value')

        self.assertRedirects(resp_post, reverse('users-directory'))
        self.assertRedirects(resp_get, reverse('users-directory'))

        self.assertTrue(message_post.type() is Message.Type.ERROR, 'Did not send correct message type')
        self.assertEqual(message_post.message(), f'You do not have permission to delete users', 'Did not return correct message')

        self.assertTrue(message_get.type() is Message.Type.ERROR, 'Did not send correct message type')
        self.assertEqual(message_get.message(), f'You do not have permission to delete users', 'Did not return correct message')

    def test_no_session(self):
        del self.session['user_id']
        self.session.save()
        resp_post = self.client.post(self.valid_delete_url, {})
        resp_get = self.client.get(self.valid_delete_url, {})

        self.assertIsNotNone(resp_post, 'Post did not return value')
        self.assertIsNotNone(resp_get, 'Get did not return value')

        self.assertRedirects(resp_post, reverse('login'))
        self.assertRedirects(resp_get, reverse('login'))

    def test_delete_removes(self):
        self.client.post(self.valid_delete_url, {}, follow=True)

        with self.assertRaises(ObjectDoesNotExist, msg='Did not remove from database'):
            User.objects.get(univ_id=self.prof_username)

from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType
from TAScheduler.viewsupport.message import Message

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

        self.valid_delete_url = reverse('user-delete', self.prof.user_id)
        self.valid_delete_self = reverse('user-delete', self.admin.user_id)
        self.invalid_delete_url = reverse('user-delete', 340000)  # Only two users were created so the max valid id is 2

        self.client.session['user_id'] = self.prof.user_id

    def test_admin_can_delete_existing(self):
        resp = self.client.post(self.valid_delete_url, {}, follow=True)

        self.assertIsNotNone(resp, 'Post did not return value')

        redirect_chain = resp.redirect_chain

        self.assertEqual(len(redirect_chain), 1, 'Did not redirect the correct number of times')
        self.assertEqual(redirect_chain[0][0], reverse('user-directory'), 'Did not redirect to user directory on delete')

        self.assertIsNotNone(resp.context['messages'], 'Did not send success message to user')
        self.assertTrue(len(resp.context['message']) >= 1, 'Did not send any success messages to user')

        message: Message = resp.context['message']

        self.assertTrue(message.type() is Message.Type.REGULAR, 'Did not send correct message type')
        self.assertEqual(message.message(), f'Successfully deleted user {self.prof_username}', 'Did not return correct message')

    def test_delete_nonexistent_redirects_with_error(self):
        pass

    def test_prof_cannot_delete_anyone(self):
        pass

    def test_delete_removes(self):
        pass

    def test_delete_redirects(self):
        pass

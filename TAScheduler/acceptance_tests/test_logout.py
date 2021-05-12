from django.test import Client, TestCase
from TAScheduler.models import User, UserType
from django.urls import reverse
from TAScheduler.viewsupport.errors import PageError, LoginError


class TestLogoutView(TestCase):

    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        self.admin_user = User.objects.create(
            username='josiahth',
            password='password',
            type=UserType.ADMIN,
            password_tmp=False
        )

    def test_logout_as_admin(self):
        self.session['user_id'] = self.admin_user.id
        self.session.save()

        resp = self.client.get(reverse('logout'))

        self.assertIsNone(resp.client.session.get('user_id', None), 'Logout did not clear the current user')

    def test_rejects_logout_not_logged_in(self):
        resp = self.client.get(reverse('logout'))

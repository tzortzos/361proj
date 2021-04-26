from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType, Course
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.errors import UserEditError



class TestCreateUserView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.session = self.client.session

        self.course_code = '361'
        self.course_name = 'Software Engineering'

        self.admin_username = 'josiahth'
        self.admin = User.objects.create(univ_id=self.admin_username,
                                         password='a-very-good-password',
                                         type=UserType.ADMIN,
                                         tmp_password=False)

        self.session['user_id'] = self.admin.user_id
        self.session.save()

    def assertContextError(self, resp) -> UserEditError:
        """Assert that a UserEditError was returned in the context and return it"""
        context = resp.context

        self.assertIsNotNone(context['error'], 'Did not return error')
        self.assertEqual(type(context['error']), UserEditError, 'Did not return correctly typed error')

        return context['error']

    # Helper method to determine whether context contains proper notification to user (of error or success)
    def assertContainsMessage(self, resp, message: Message, msg: str = 'Message object was not in context'):
        self.assertTrue(message in MessageQueue.get(resp.client.session), msg=msg)

    def test_rejects_empty_course_code(self):
        resp = self.client.post(reverse('courses-create'), {
            'course_code': '',
            'course_name': self.course_name

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response.')

        ret_error = self.assertContextError(resp)

        # TODO: update place() with CODE error
        self.assertTrue(ret_error.place() is UserEditError.Place.CODE, 'Did not recognize that course code was empty.')
        self.assertEqual(ret_error.error().body(), 'Course Code must be exactly 3 digits in length')

    def test_rejects_non_three_digit_course_code(self):
        resp = self.client.post(reverse('courses-create'), {
            'course_code': '12nfu',
            'course_name': self.course_name

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response.')

        ret_error = self.assertContextError(resp)

        # TODO: update place() with CODE error
        self.assertTrue(ret_error.place() is UserEditError.Place.CODE, 'Did not recognize that course code was empty.')
        self.assertEqual(ret_error.error().body(), 'Course Code must be exactly 3 digits in length')


    def test_rejects_empty_course_name(self):
        resp = self.client.post(reverse('courses-create'), {
            'course_code': self.course_code,
            'course_name': ''

        }, follow=False)

        self.assertIsNotNone(resp, 'Did not return a response.')

        ret_error = self.assertContextError(resp)

        # TODO: update place() with NAME error
        self.assertTrue(ret_error.place() is UserEditError.Place.NAME, 'Did not recognize that course name was empty.')
        self.assertEqual(ret_error.error().body(), 'Course Name must be entered in full.')


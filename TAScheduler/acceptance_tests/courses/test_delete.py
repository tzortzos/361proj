from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import CourseEditError, CourseEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab


class CourseDeletes(TASAcceptanceTestCase[CourseEditError]):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        # Add user
        self.admin_user = User.objects.create(
            univ_id='josiahth',
            password='password',
            type=UserType.ADMIN,
            tmp_password=False
        )


        self.course = Course.objects.create(course_code='351', course_name='DSA')

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()
        self.url = reverse('courses-delete')
        self.course = Course.objects.create(course_code='351', course_name='DSA')

    def test_delete_with_message(self):

        resp = self.client.post(self.url, {
            'course_id': self.course
        })

        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(course_id=self.course.section)

        self.assertContainsMessage(resp, Message('Course 351 DSA deleted successfully'), Message.Type.ERROR)
        self.assertRedirects(resp, reverse('courses-directory'))

from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import CourseError
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab


class CourseDeletes(TASAcceptanceTestCase[CourseError]):
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
        self.session['user_id'] = self.admin_user.user_id
        self.session.save()

    def test_delete_with_message(self):

        resp = self.client.post(reverse('courses-delete', args=[self.course.course]))

        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(course_id=self.course.course)

        self.assertContainsMessage(resp, Message('Course 351 DSA deleted successfully'))

        self.assertRedirects(resp, reverse('courses-directory'))

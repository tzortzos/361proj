from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import CourseEditError, CourseEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab
from django.db.models import ObjectDoesNotExist


class CourseDeletes(TASAcceptanceTestCase[CourseEditError]):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        # Add user
        self.admin_user = User.objects.create(
            username='josiahth',
            password='password',
            type=UserType.ADMIN,
            password_tmp=False
        )

        self.course = Course.objects.create(
            code='351',
            name='DSA',
        )

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()
        self.url = reverse('courses-delete', args=[self.course.id])

    def test_delete_with_message(self):

        resp = self.client.post(self.url, {
            'course_id': self.course
        })

        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(id=self.course.id)

        self.assertContainsMessage(resp, Message(f'Course {self.course.code} {self.course.name} deleted successfully'))
        self.assertRedirects(resp, reverse('courses-directory'))

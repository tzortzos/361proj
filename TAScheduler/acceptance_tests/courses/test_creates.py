from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import CourseEditError, CourseEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab


class CourseCreates(TASAcceptanceTestCase[CourseEditError]):

    def setUp(self) -> None:
        self.client = Client()
        self.session = self.client.session

        # Add user
        self.admin_user = User.objects.create(
            univ_id='josiahth',
            password='password',
            type=UserType.ADMIN,
            tmp_password=False
        )

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()

        self.good_code = '361'
        self.good_name = 'Software Engineering'

        self.url = reverse('courses-create')

    def test_creates(self):
        resp = self.client.post(self.url, {
            'course_code': self.good_code,
            'course_name': self.good_name,
        })

        course = list(Course.objects.all())[0]

        self.assertRedirects(resp, reverse('courses-view', args=[course.section]))

        self.assertEqual(self.good_code, course.code)
        self.assertEqual(self.good_name, course.name)

    def test_rejects_missing_code(self):
        resp = self.client.post(self.url, {
            # 'course_code': self.good_code,
            'course_name': self.good_name,
        })

        error = self.assertContextError(resp)

        self.assertEqual(CourseEditPlace.CODE, error.place())
        self.assertEqual('you must input a 3 digit course code', error.message())

    def test_rejects_short_code(self):
        resp = self.client.post(self.url, {
            'course_code': self.good_code[:2],
            'course_name': self.good_name,
        })

        error = self.assertContextError(resp)

        self.assertEqual(CourseEditPlace.CODE, error.place())
        self.assertEqual('A course code must be exactly 3 digits', error.message())

    def test_rejects_missing_name(self):
        resp = self.client.post(self.url, {
            'course_code': self.good_code,
            # 'course_name': self.good_name,
        })

        error = self.assertContextError(resp)

        self.assertEqual(CourseEditPlace.CODE, error.place())
        self.assertEqual('You must provide a course name', error.message())

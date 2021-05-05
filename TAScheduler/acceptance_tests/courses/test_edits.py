from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import CourseEditError, CourseEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab


class CourseEdit(TASAcceptanceTestCase[CourseEditError]):

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

        self.course = Course.objects.create(course_code='351', course_name='DSA')

        self.edit_url = reverse('courses-edit', args=[self.course.section])
        self.view_url = reverse('courses-view', args=[self.course.section])
        self.good_code = '361'
        self.good_name = 'Software Engineering'
        self.good_name2 = 'Data Structures and Algorithms'
        self.good_code2 = '351'

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()

    def test_edits(self):
        resp = self.client.post(self.edit_url, {
            'course_code': self.good_code,
            'course_name': self.good_name,
        })

        self.assertRedirects(resp, self.view_url)

        self.course.refresh_from_db()

        self.assertEqual(self.good_code, self.course.code, msg='Did not save code to database')
        self.assertEqual(self.good_name, self.course.name, msg='Did not save course name to database')

    def test_rejects_missing_code(self):
        resp = self.client.post(self.edit_url, {
            # 'course_code': self.good_code2,
            'course_name': self.good_name2,
        })

        error = self.assertContextError(resp)

        self.assertEqual(CourseEditPlace.CODE, error.place())
        self.assertEqual('You cannot remove a course code', error.message())

    def test_rejects_short_code(self):
        resp = self.client.post(self.edit_url, {
            'course_code': self.good_code[:2],
            'course_name': self.good_name2,
        })

        error = self.assertContextError(resp)

        self.assertEqual(CourseEditPlace.CODE, error.place())
        self.assertEqual('A course code must be exactly 3 digits', error.message())

    def test_rejects_missing_name(self):
        resp = self.client.post(self.edit_url, {
            'course_code': self.good_code2,
            # 'course_name': self.good_name2,
        })

        error = self.assertContextError(resp)

        self.assertEqual(CourseEditPlace.NAME, error.place())
        self.assertEqual('You cannot remove the course name', error.message())

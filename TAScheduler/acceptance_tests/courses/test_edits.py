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

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()

    def test_edits(self):
        resp = self.client.post(self.edit_url, {
            'course_code': '361',
            'course_name': 'Software Engineering',
        })

        self.assertRedirects(resp, self.view_url)

        self.course.refresh_from_db()

        self.assertEqual('361', self.course.code, msg='Did not save code to database')
        self.assertEqual('Software Engineering', self.course.name, msg='Did not save course name to database')

    def test_rejects_missing_code(self):
        resp = self.client.post(self.edit_url, {
            # 'course_code': '351',
            'course_name': 'Data Structures and Algorithms',
        })

        error = self.assertContextError(resp)

        self.assertEqual('You cannot remove a course code', error.message(), 'Did not return correct error message')
        self.assertEqual(CourseEditPlace.CODE, error.place(),
                         'Did not associate incorrect code with correct place')

    def test_rejects_short_code(self):
        resp = self.client.post(self.edit_url, {
            'course_code': '35',
            'course_name': 'Data Structures and Algorithms',
        })

        error = self.assertContextError(resp)

        self.assertEqual('A course code must be exactly 3 digits', error.message(),
                         'Did not return correct error message')
        self.assertEqual(CourseEditPlace.CODE, error.place(),
                         'Did not associate incorrect code with correct place')

    def test_rejects_missing_name(self):
        resp = self.client.post(self.edit_url, {
            'course_code': '351',
            # 'course_name': 'Data Structures and Algorithms',
        })

        error = self.assertContextError(resp)

        self.assertEqual('You cannot remove the course name', error.message(),
                         'Did not return correct error message')
        self.assertEqual(CourseEditPlace.NAME, error.place(),
                         'Did not associate incorrect code with correct place')

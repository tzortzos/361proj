from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import CourseError
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, CourseSection, LabSection


class CourseCreates(TASAcceptanceTestCase[CourseError]):

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
        self.session['user_id'] = self.admin_user.user_id
        self.session.save()

    def test_creates(self):
        resp = self.client.post(reverse('courses-create'), {
            'course_code': '351',
            'course_name': 'Data Structures and Algorithms',
        })

        course = list(Course.objects.all())[0]

        self.assertRedirects(resp, reverse('courses-view', args=[course.course_id]))

        self.assertEqual('351', course.course_code, msg='Did not save code to database')
        self.assertEqual('Data Structures and Algorithms', course.course_name, msg='Did not save course name to database')

    def test_rejects_missing_code(self):
        resp = self.client.post(reverse('courses-create'), {
            # 'course_code': '351',
            'course_name': 'Data Structures and Algorithms',
        })

        error = self.assertContextError(resp)

        self.assertEqual('A course code must be exactly 3 digits', error.error(), 'Did not return correct error message')
        self.assertEqual(CourseError.Place.CODE, error.place(), 'Did not associate incorrect code with correct place')

    def test_rejects_short_code(self):
        resp = self.client.post(reverse('courses-create'), {
            'course_code': '35',
            'course_name': 'Data Structures and Algorithms',
        })

        error = self.assertContextError(resp)

        self.assertEqual('A course code must be exactly 3 digits', error.error(),
                         'Did not return correct error message')
        self.assertEqual(CourseError.Place.CODE, error.place(), 'Did not associate incorrect code with correct place')

    def test_rejects_missing_name(self):
        resp = self.client.post(reverse('courses-create'), {
            'course_code': '351',
            # 'course_name': 'Data Structures and Algorithms',
        })

        error = self.assertContextError(resp)

        self.assertEqual('You must provide a course name', error.error(),
                         'Did not return correct error message')
        self.assertEqual(CourseError.Place.NAME, error.place(), 'Did not associate incorrect code with correct place')

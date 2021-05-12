from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType, Course, Section
from TAScheduler.viewsupport.errors import SectionEditError, SectionEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase


class CreateSection(TASAcceptanceTestCase[SectionEditError]):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        self.admin_user = User.objects.create(
            username='josiahth',
            password='good-password',
            type=UserType.ADMIN,
            password_tmp=False,
        )

        self.course = Course.objects.create(
            code='361',
            name='Software Engineering',
        )

        self.session['user_id'] = self.admin_user.id
        self.session.save()

        self.good_code = '901'
        self.bad_course_id = '-1'

        self.url = reverse('sections-create')

    def test_adds_to_database(self):
        resp = self.client.post(self.url, {
            'section_code': self.good_code,
            'course_id': self.course.id
        })

        section = list(Section.objects.all())[0]

        self.assertRedirects(resp, reverse('sections-view', args=[section.id]))

        self.assertEqual(self.good_code, section.code)
        self.assertEqual(self.course, section.id)

    def test_redirects_on_success(self):
        resp = self.client.post(self.url, {
            'section_code': self.good_code,
            'course_id': self.course.id,
        })

        section = list(Section.objects.all())[0]

        self.assertRedirects(
            resp,
            reverse('sections-view', args=[section.id])
        )

    def test_rejects_missing_section_code(self):
        resp = self.client.post(self.url, {
            # 'section_code': self.good_code,
            'course_id': self.course.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(SectionEditPlace.CODE, error.place())
        self.assertEqual('You must input a 3 digit section code', error.message())

    def test_rejects_missing_course_id(self):
        # The course_id should always exist, but the default value is
        # -1 which is used as our invalidity sigill as the database will
        # never user that value as a course_id
        resp = self.client.post(self.url, {
            'section_code': self.good_code,
            # 'course_id': self.good_name,
        })
        error = self.assertContextError(resp)

        self.assertEqual(SectionEditPlace.COURSE, error.place())
        self.assertEqual('You must select a course for this section', error.message())

    def test_rejects_invalid_course_id(self):
        # The course_id should always exist, but the default value is
        # -1 which is used as our invalidity sigill as the database will
        # never user that value as a course_id
        resp = self.client.post(self.url, {
            'section_code': self.good_code,
            'course_id': self.bad_course_id,
        })
        error = self.assertContextError(resp)

        self.assertEqual(SectionEditPlace.COURSE, error.place())
        self.assertEqual('-1 isn not a valid course id', error.message())
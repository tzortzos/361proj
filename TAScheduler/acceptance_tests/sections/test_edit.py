from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist
from django.shortcuts import reverse

from TAScheduler.models import User, UserType, Course, Section
from TAScheduler.viewsupport.errors import SectionEditError, SectionEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase


class SectionEdit(TASAcceptanceTestCase[SectionEditError]):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        self.admin_user = User.objects.create(
            username='josiahth',
            password='good-password',
            type=UserType.ADMIN,
            password_tmp=False,
        )

        self.section = Section.objects.create(
            code='902',
            course='Software Engineering',
        )

        self.session['user_id'] = self.admin_user.id
        self.session.save()

        self.good_code = '901'

        self.edit_url = reverse('sections-edit', args=[self.section])
        self.view_url = reverse('sections-view', args=[self.section])

    def test_edits(self):
        resp = self.client.post(self.edit_url, {
            'section_code': self.good_code,
            'course_id': self.course.id,
        })

        self.assertRedirects(resp, self.view_url)

        self.section.refresh_from_db()

        self.assertEqual(self.good_code, self.section.code)
        self.assertEqual(self.course.id, self.section.section)

    def test_rejects_missing_code(self):
        resp = self.client.post(self.edit_url, {
            # 'course_code': self.good_code,
            'course_id': self.course.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(SectionEditPlace.CODE, error.place())
        self.assertEqual('You cannot remove a course code', error.message())

    def test_rejects_short_code(self):
        resp = self.client.post(self.edit_url, {
            'course_code': self.good_code[:2],
            'course_id': self.course.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(SectionEditPlace.CODE, error.place())
        self.assertEqual('A section code must be exactly 3 digits', error.message())


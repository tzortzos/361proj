from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

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

        self.course = Course.objects.create(
            code='361',
            course='Software Engineering',
        )

        self.session['user_id'] = self.admin_user.id
        self.session.save()

        self.good_code = '901'
        self.good_name = 'Software Engineering'

        self.url = reverse('sections-edit')

    def test_edits(self):
        resp = self.client.post(self.url, {
            'section_code': self.good_code,
            'course_name': self.good_name,
        })

        self.assertRedirects(resp, self.view_url)

        self.course.refresh_from_db()

        self.assertEqual('361', self.course.code, msg='Did not save code to database')
        self.assertEqual('Software Engineering', self.course.name, msg='Did not save course name to database')
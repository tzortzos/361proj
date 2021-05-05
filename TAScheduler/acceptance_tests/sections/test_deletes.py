from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType, Course, Section
from TAScheduler.viewsupport.errors import SectionEditError, SectionEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase


class SectionDeletes(TASAcceptanceTestCase[SectionEditError]):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        # Add user
        self.admin_user = User.objects.create(
            username='josiahth',
            password='good-password',
            type=UserType.ADMIN,
            password_tmp=False,
        )

        self.course = Course.objects.create(code='361', course='Software Engineering')

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()

    def test_deletes_from_database(self):
        resp = self.client.post(reverse('sections-delete', args=[self.course.section.id]))

        with self.assertRaises(Course.DoesNotExist):
            Section.objects.get(section_id=self.course.section.id)

        self.assertRedirects(resp, reverse('section-view'))
        self.assertContainsMessage(resp, Message('Course 361 Software Engineering deleted successfully'))

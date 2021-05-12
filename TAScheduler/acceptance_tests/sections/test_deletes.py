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

        self.section = Section.objects.create(code='901', course='Software Engineering')

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()

    def test_deletes_from_database(self):
        resp = self.client.post(reverse('sections-delete', args=[self.section.id]))

        with self.assertRaises(Section.DoesNotExist):
            Section.objects.get(section_id=self.section.id)

        self.assertRedirects(resp, reverse('sections-view'))
        self.assertContainsMessage(resp, Message('Section 901 of Software Engineering deleted successfully'))

from django.test import Client
from django.shortcuts import reverse

from typing import List

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabEditError, LabEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab


class LabsDirectory(TASAcceptanceTestCase[LabEditError]):

    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        # Add users
        self.admin_user = User.objects.create(
            username='josiahth',
            password='password',
            type=UserType.ADMIN,
            password_tmp=False
        )

        self.ta_user = User.objects.create(
            username='nleverence',
            password='password',
            type=UserType.TA,
            password_tmp=False
        )

        # Add prerequisite objects
        self.course = Course.objects.create(
            code='361',
            name='Software Engineering',
        )

        self.section = Section.objects.create(
            code='201',
            course=self.course,
        )

        self.lab_partial = Lab.objects.create(
            code='901',
            section=self.section,
        )

        self.lab_full = Lab.objects.create(
            code='902',
            section=self.section,
            day='MWF',
            time='2-4',
            ta=self.ta_user,
        )

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()

        self.good_code = '901'

        self.url = reverse('labs-directory')

    def test_context_contains_labs(self):
        resp = self.client.get(self.url)

        labs: List[object] = resp.context.get('labs')

        for li in range(len(labs)):
            self.assertTrue(isinstance(labs[li], Lab), msg='Returned non lab object')

        self.assertEqual(2, len(labs), 'Did not return the correct number of lab arguments')


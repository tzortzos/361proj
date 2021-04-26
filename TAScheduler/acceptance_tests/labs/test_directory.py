from django.test import Client
from django.shortcuts import reverse

from typing import List

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabError
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, CourseSection, LabSection


class LabsDelete(TASAcceptanceTestCase[LabError]):

    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        # Add users
        self.admin_user = User.objects.create(
            univ_id='josiahth',
            password='password',
            type=UserType.ADMIN,
            tmp_password=False
        )

        # Add prerequisite objects
        self.course = Course.objects.create(
            course_code='361',
            course_name='Software Engineering',
            admin_id=self.admin_user,
        )

        self.section = CourseSection.objects.create(
            course_section_code='201',
            course_id=self.course,
        )

        self.lab_partial = LabSection.objects.create(
            lab_section_code='901',
            course_section_id=self.section,
        )

        self.lab_full = LabSection.objects.create(
            lab_section_code='901',
            course_section_id=self.section,
            lab_days='MWF',
            lab_time='2-4',
            ta_id=self.ta_user,
        )

        # Set current user
        self.session['user_id'] = self.admin_user.user_id
        self.session.save()

    def test_context_contains_labs(self):
        resp = self.client.get(reverse('labs-directory'))

        labs = resp.context.getlist('labs')

        for li in range(len(labs)):
            self.assertTrue(isinstance(labs[li], LabSection), msg='Returned non lab object')

        self.assertEqual(2, len(labs), 'Did not return the correct number of lab arguments')


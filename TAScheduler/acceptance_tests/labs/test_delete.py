from django.test import Client
from django.shortcuts import reverse

from typing import List

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabError
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, CourseSection, Lab


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

        self.ta_user = User.objects.create(
            univ_id='nleverence',
            password='password',
            type=UserType.TA,
            tmp_password=False
        )

        self.prof_user = User.objects.create(
            univ_id='rock',
            password='password',
            type=UserType.PROF,
            tmp_password=False
        )

        self.section = CourseSection.objects.create(
            course_section_code='201',
            course_id=self.course,
        )

        self.lab_partial = Lab.objects.create(
            lab_section_code='901',
            course_section_id=self.section,
        )

        self.lab_full = Lab.objects.create(
            lab_section_code='902',
            course_section_id=self.section,
            lab_days='MWF',
            lab_time='2-4',
            ta_id=self.ta_user,
        )

        # Set current user
        self.session['user_id'] = self.admin_user.user_id
        self.session.save()

    def test_redirects_professor(self):
        self.session['user_id'] = self.prof_user.user_id
        self.session.save()

        resp = self.client.post(reverse('labs-delete', args=[self.lab_full.id]))

        self.assertContainsMessage(resp, Message(
            'You do not have permission to delete lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_redirects_ta(self):
        self.session['user_id'] = self.ta_user.user_id
        self.session.save()

        resp = self.client.post(reverse('labs-delete', args=[self.lab_full.id]))

        self.assertContainsMessage(resp, Message(
            'You do not have permission to delete lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_removes_database(self):
        resp = self.client.post(reverse('labs-delete', args=[self.lab_full.id]))

        labs: List[Lab] = list(Lab.objects.all())

        self.assertEqual(1, len(labs), 'Did not remove lab section')

        self.assertContainsMessage(resp, Message(
            'Successfully deleted lab section'
        ))

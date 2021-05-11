from django.test import Client
from django.shortcuts import reverse

from typing import List

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabEditError, LabEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab


class LabsDelete(TASAcceptanceTestCase[LabEditError]):

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

        # Add prerequisite objects
        self.course = Course.objects.create(
            code='361',
            name='Software Engineering',
        )

        self.ta_user = User.objects.create(
            username='nleverence',
            password='password',
            type=UserType.TA,
            password_tmp=False
        )

        self.prof_user = User.objects.create(
            username='rock',
            password='password',
            type=UserType.PROF,
            password_tmp=False
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
        self.url = reverse('labs-delete', args=[self.lab_full.id])

    def test_redirects_professor(self):
        self.session['user_id'] = self.prof_user.id
        self.session.save()

        resp = self.client.post(self.url, {
            'lab_id': self.lab_full
        })

        self.assertContainsMessage(resp, Message(
            'You do not have permission to delete lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_redirects_ta(self):
        self.session['user_id'] = self.ta_user.id
        self.session.save()

        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            'section_id': self.section.id,
        })

        self.assertContainsMessage(resp, Message(
            'You do not have permission to delete lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_removes_database(self):
        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            'section_id': self.section.id,
        })

        labs: List[Lab] = list(Lab.objects.all())

        self.assertEqual(1, len(labs), 'Did not remove lab section')

        self.assertContainsMessage(resp, Message(
            'Successfully deleted lab section'
        ))

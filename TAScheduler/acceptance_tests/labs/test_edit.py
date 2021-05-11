from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabEditError, LabEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab

class LabsEdit(TASAcceptanceTestCase[LabEditError]):

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

        self.prof_user = User.objects.create(
            username='rock',
            password='password',
            type=UserType.PROF,
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
        self.non_digit_code = 'abc'
        self.mislen_code = '90103'

        self.url = reverse('labs-edit', args=[self.lab_partial.id])

    def test_ta_redirects(self):
        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            'section_id': self.section,
        })

        self.assertContainsMessage(resp, Message(
            'You do not have permission to edit lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    # TODO needs the positive cases for updating existing, as well as removing things

    def test_rejects_remove_code(self):
        resp = self.client.post(self.url, {
            # 'lab_code': '901',
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

    def test_rejects_non_digit_code(self):
        resp = self.client.post(self.url, {
            'lab_code': self.non_digit_code,
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

    def test_rejects_mislengthed_code(self):
        # Test that code lengths must be 3
        resp = self.client.post(self.url, {
            'lab_code': self.mislen_code,
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

        resp = self.client.post(self.url, {
            'lab_code': '9',
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabError
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, CourseSection, LabSection

class LabsEdit(TASAcceptanceTestCase[LabError]):

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
            lab_section_code='902',
            course_section_id=self.section,
            lab_days='MWF',
            lab_time='2-4',
            ta_id=self.ta_user,
        )

        # Set current user
        self.session['user_id'] = self.admin_user.user_id
        self.session.save()

    def test_ta_redirects(self):
        self.session['user_id'] = self.ta_user.user_id
        self.session.save()

        resp = self.client.post(reverse('labs-edit', args=[self.lab_partial.lab_section_id]), {
            'lab_code': '901',
            'section_id': self.section.course_section_id,
        })

        self.assertContainsMessage(resp, Message(
            'You do not have permission to edit lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    # TODO needs the positive cases for updating existing, as well as removing things

    def test_rejects_remove_code(self):
        resp = self.client.post(reverse('labs-edit', args=[self.lab_partial.lab_section_id]), {
            # 'lab_code': '901',
            'section_id': self.section.course_section_id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

    def test_rejects_non_digit_code(self):
        resp = self.client.post(reverse('labs-edit', args=[self.lab_partial.lab_section_id]), {
            'lab_code': 'abc',
            'section_id': self.section.course_section_id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

    def test_rejects_mislengthed_code(self):
        # Test that code lengths must be 3
        resp = self.client.post(reverse('labs-edit', args=[self.lab_partial.lab_section_id]), {
            'lab_code': '90103',
            'section_id': self.section.course_section_id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

        resp = self.client.post(reverse('labs-edit', args=[self.lab_partial.lab_section_id]), {
            'lab_code': '9',
            'section_id': self.section.course_section_id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You cannot remove the 3 digit lab code', error.error(), 'Did not return correct message')

from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabError
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, CourseSection, Lab


class LabsCreate(TASAcceptanceTestCase[LabError]):

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

        # Set current user
        self.session['user_id'] = self.admin_user.user_id
        self.session.save()

    def test_create_without_days_times(self):
        resp = self.client.post(reverse('labs-create'), {
            'lab_code': '901',
            'section_id': self.section.course,
        })

        labs = list(Lab.objects.all())[0]

        self.assertEqual('901', labs.code, 'Did not save lab section code to database')
        self.assertEqual(self.section, labs.course, 'Did not associate correct course section with new lab')

        self.assertRedirects(resp, reverse('labs-view', args=[labs.id]))

    def test_create_full(self):
        resp = self.client.post(reverse('labs-create'), {
            'lab_code': '901',
            'section_id': self.section.course,
            'lab_day': 'M',
            'lab_time': '2-4',
        })

        lab = list(Lab.objects.all())[0]

        self.assertEqual('M', lab.day, f'Day \'M\' not saved to lab')

        self.assertEqual('2-4', lab.time, 'Did not save correct time to database')

        self.assertRedirects(resp, reverse('labs-view', args=[lab.id]))

    def test_professor_rejected(self):
        self.session['user_id'] = self.prof_user.user_id
        self.session.save()

        resp = self.client.post(reverse('labs-create'), {
            'lab_code': '901',
            'section_id': self.section.course,
        })

        self.assertContainsMessage(resp, Message(
            'You do not have permission to create new lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_ta_redirects(self):
        self.session['user_id'] = self.ta_user.user_id
        self.session.save()

        resp = self.client.post(reverse('labs-create'), {
            'lab_code': '901',
            'section_id': self.section.course,
        })

        self.assertContainsMessage(resp, Message(
            'You do not have permission to create new lab sections',
            Message.Type.ERROR,
        ))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_rejects_missing_code(self):
        resp = self.client.post(reverse('labs-create'), {
            # 'lab_code': '901',
            'section_id': self.section.course,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You must provide a 3 digit lab code', error.error(), 'Did not return correct message')

    def test_rejects_non_digit_code(self):
        resp = self.client.post(reverse('labs-create'), {
            'lab_code': 'abc',
            'section_id': self.section.course,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You must provide a 3 digit lab code', error.error(), 'Did not return correct message')

    def test_rejects_mislengthed_code(self):
        resp = self.client.post(reverse('labs-create'), {
            'lab_code': '90103',
            'section_id': self.section.course,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You must provide a 3 digit lab code', error.error(), 'Did not return correct message')

        resp = self.client.post(reverse('labs-create'), {
            'lab_code': '9',
            'section_id': self.section.course,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.CODE, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You must provide a 3 digit lab code', error.error(), 'Did not return correct message')

    def test_rejects_missing_section(self):
        resp = self.client.post(reverse('labs-create'), {
            'lab_code': '901',
            # 'section_id': self.section.course_section_id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabError.Place.SECTION, error.place(), 'Did not associate error with correct field')
        self.assertEqual('You must pick a section for this lab', error.error(), 'Did not return correct message')

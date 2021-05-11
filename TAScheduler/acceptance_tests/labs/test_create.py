from django.test import Client
from django.shortcuts import reverse

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabEditError, LabEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue

from TAScheduler.models import User, UserType, Course, Section, Lab


class LabsCreate(TASAcceptanceTestCase[LabEditError]):

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

        # Add prerequisite objects had a question about this
        self.course = Course.objects.create(
            code='361',
            name='Software Engineering',
        )

        self.section = Section.objects.create(
            code='201',
            course=self.course,
        )

        # Set current user
        self.session['user_id'] = self.admin_user.id
        self.session.save()

        self.good_code = '901'
        self.good_name = 'Software Engineering'
        self.good_day = 'M'
        self.good_time = '2-4'

        self.non_digit_code = 'abc'
        self.mislen_code = '90103'

        self.url = reverse('labs-create')

    def test_create_without_days_times(self):
        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            'section_id': self.section.id,
        })

        labs = list(Lab.objects.all())[0]

        self.assertEqual(self.good_code, labs.code, 'Did not save lab section code to database')
        self.assertEqual(self.section, labs.section, 'Did not associate correct course section with new lab')

        self.assertRedirects(resp, reverse('labs-view', args=[labs.id]))

    def test_create_full(self):
        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            'section_id': self.section.id,
            'lab_day': self.good_day,
            'lab_time': self.good_time,
        })

        lab = list(Lab.objects.all())[0]

        self.assertEqual(self.good_day, lab.day, f'Day \'M\' not saved to lab')

        self.assertEqual(self.good_time, lab.time, 'Did not save correct time to database')

        self.assertRedirects(resp, reverse('labs-view', args=[lab.id]))

    def test_professor_rejected(self):
        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            'section_id': self.section.id,
        })
        print(resp)
        # self.assertContainsMessage(resp, Message(
        #         'You do not have permission to create new lab sections',
        #         Message.Type.ERROR,
        #     ))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_ta_redirects(self):
        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            'section_id': self.section.id,
        })

        self.assertContainsMessage(resp, Message('You do not have permission to create new lab sections', Message.Type.ERROR))

        self.assertRedirects(resp, reverse('labs-directory'))

    def test_rejects_missing_code(self):
        resp = self.client.post(self.url, {
            # 'lab_code': '901',
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditPlace.CODE, error.place())
        self.assertEqual('You must provide a 3 digit lab code', error.message())

    def test_rejects_non_digit_code(self):
        resp = self.client.post(self.url, {
            'lab_code': self.non_digit_code,
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditPlace.CODE, error.place())
        self.assertEqual('You must provide a 3 digit lab code', error.message())

    def test_rejects_mislengthed_code(self):
        resp = self.client.post(self.url, {
            'lab_code': self.mislen_code,
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditPlace.CODE, error.place())
        self.assertEqual('You must provide a 3 digit lab code', error.message())

        resp = self.client.post(self.url, {
            'lab_code': '9',
            'section_id': self.section.id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditPlace.CODE, error.place())
        self.assertEqual('You must provide a 3 digit lab code', error.message())

    def test_rejects_missing_section(self):
        resp = self.client.post(self.url, {
            'lab_code': self.good_code,
            # 'section_id': self.section.course_section_id,
        })

        error = self.assertContextError(resp)

        self.assertEqual(LabEditPlace.SECTION, error.place())
        self.assertEqual('You must pick a section for this lab', error.message())

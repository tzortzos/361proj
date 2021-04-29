from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType, Course, Section
from TAScheduler.viewsupport.errors import SectionError
from TAScheduler.viewsupport.message import Message, MessageQueue


class CreateSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = self.client.session

        self.user = User.objects.create(
            univ_id='josiahth',
            password='good-password',
            type=UserType.ADMIN,
            tmp_password=False,
        )

        self.course = Course.objects.create(
            course_code='361',
            course_name='Software Engineering',
            admin_id=self.user,
        )

        self.session['user_id'] = self.user.user_id
        self.session.save()

    def assertContainsMessage(self, resp, message: Message, msg: str = 'Message object was not in context'):
        self.assertTrue(message in MessageQueue.get(resp.client.session), msg=msg)

    def assertContextError(self, resp) -> SectionError:
        """Assert that a UserEditError was returned in the context and return it"""
        context = resp.context

        self.assertIsNotNone(context['error'], 'Did not return error')
        self.assertEqual(type(context['error']), SectionError, 'Did not return correctly typed error')

        return context['error']

    def test_adds_to_database(self):
        resp = self.client.post(reverse('sections-create'), {
            'section_code': '901',
            'course_id': self.course.course,
        })

        section = list(Section.objects.all())

        self.assertEqual(1, len(section), 'Did not create course section in database')

        section = section[0]

        self.assertEqual('901', section.code, 'Did not save section code to database')
        self.assertEqual(self.course, section.course, 'Did not save course to database')

    def test_redirects_on_success(self):
        resp = self.client.post(reverse('sections-create'), {
            'section_code': '901',
            'course_id': self.course.course,
        })

        section = list(Section.objects.all())[0]

        self.assertRedirects(
            resp,
            reverse('sections-view', args=(section.course,))
        )

    def test_rejects_missing_section_code(self):
        resp = self.client.post(reverse('sections-create'), {
            'course_id': self.course.course,
        })

        context_error = self.assertContextError(resp)

        self.assertEqual(
            'You must input a 3 digit section code',
            context_error.error().body(),
            msg='Did not reject missing section code with correct message'
        )

        self.assertEqual(
            SectionError.Place.CODE,
            context_error.place(),
            msg='Did not reject missing course code with error message in correct place',
        )

    def test_rejects_missing_course_id(self):
        # The course_id should always exist, but the default value is
        # -1 which is used as our invalidity sigill as the database will
        # never user that value as a course_id
        resp = self.client.post(reverse('sections-create'), {
            'section_code': '901',
            'course_id': '-1',
        })

        context_error = self.assertContextError(resp)

        self.assertEqual(
            'You must select a course for this section',
            context_error.error().body(),
            msg='Did not reject incorrect course id with correct message',
        )

        self.assertEqual(
            SectionError.Place.COURSE,
            context_error.place(),
            msg='Did not place rejection message on correct field for incorrect course id'
        )

from django.shortcuts import reverse, redirect
from django.test import Client

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.models import User, UserType, Skill
from TAScheduler.viewsupport.message import Message, MessageQueue

class SkillsCreate(TASAcceptanceTestCase[()]):

    def setUp(self):
        self.client = Client
        self.session = self.client.session

        self.user_admin = User.objects.create(
            username='lnahnan',
            type=UserType.ADMIN,
            password='password',
            password_tmp=False,
        )

        self.session['user_id'] = self.user_admin.id
        self.session.save()

        self.skill_name = 'Django Models'
        self.long_skill_name = 'A very long skill name that should be rejected by the view'

        self.url = reverse('skills-create')

    def test_creates_new(self):
        resp = self.client.post(self.url, {
            'new_skill': self.skill_name,
        })

        self.assertRedirects(resp, reverse('skills-directory'))

        skills_list = list(Skill.objects.all())

        self.assertEqual(1, len(skills_list), msg='Did not create the skill correctly')

        self.assertEqual(
            self.skill_name,
            skills_list[0].name,
            msg='Did not save skill name correctly'
        )

    def test_does_not_crash_on_creating_existing_skill(self):
        resp = self.client.post(self.url, {
            'new_skill': self.skill_name,
        })

        self.assertRedirects(resp, reverse('skills-directory'))

        resp = self.client.post(self.url, {
            'new_skill': self.skill_name,
        })

        self.assertEqual(
            0,
            len(MessageQueue.get(resp.client.session)),
            msg='Should not send message on recreation of a skill'
        )

        self.assertRedirects(resp, reverse('skills-directory'))

        skills_list = list(Skill.objects.all())

        self.assertEqual(1, len(skills_list), msg='Seems to have recreated the skill')

        self.assertEqual(
            self.skill_name,
            skills_list[0].name,
            msg='Did not save skill name correctly'
        )

    def test_rejects_too_long(self):
        resp = self.client.post(self.url, {
            'new_skill': self.long_skill_name,
        })

        self.assertContainsMessage(
            resp,
            Message(
                'A skills name may not be more than 30 characters',
                Message.Type.ERROR,
            )
        )

        self.assertRedirects(resp, reverse('skills-directory'))

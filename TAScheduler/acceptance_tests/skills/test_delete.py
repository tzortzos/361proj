from django.shortcuts import reverse, redirect
from django.test import Client
from django.contrib.sessions.backends.base import SessionBase

from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.models import User, UserType, Skill
from TAScheduler.viewsupport.message import Message, MessageQueue


class SkillsDelete(TASAcceptanceTestCase[object]):

    def setUp(self) -> None:
        self.client = Client()
        self.session: SessionBase = self.client.session

        self.user_admin = User.objects.create(
            username='lnahnan',
            type=UserType.ADMIN,
            password='password',
            password_tmp=False,
        )

        self.session['user_id'] = self.user_admin.id
        self.session.save()

        self.skill = Skill.objects.create(
            name='Django Models',
        )

        self.url = reverse('skills-delete', args=[self.skill.id])
        self.url_bad = reverse('skills-delete', args=[self.skill.id + 1])

    def test_delete_exiting(self):
        resp = self.client.get(self.url, {})

        self.assertContainsMessage(
            resp,
            Message(
                f'Skill \'{self.skill.name}\' deleted',
            )
        )

        self.assertRedirects(resp, reverse('skills-directory'))

    def test_delete_nonexistent(self):
        resp = self.client.get(self.url_bad, {})

        self.assertContainsMessage(
            resp,
            Message(
                'Cannot delete nonexistent skill',
                Message.Type.ERROR,
            )
        )

        self.assertRedirects(resp, reverse('skills-directory'))

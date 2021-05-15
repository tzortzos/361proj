from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.models import Skill
from TAScheduler.ClassDesign.LoginUtility import LoginUtility, UserType
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.ClassDesign.SkillsUtility import Skill, SkillsUtility


class SkillsCreate(View):

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('index'),
            Message('You do not have permission to edit skills', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        new_skill: str = request.POST.get(key='new_skill', default='')

        # Do not try to create empty skills
        if new_skill == '':
            return redirect(reverse('skills-directory'))

        if not SkillsUtility.create_skill(new_skill):
            MessageQueue.push(
                request.session,
                Message(
                    'A skills name may not be more than 30 characters',
                    Message.Type.ERROR,
                )
            )

        return redirect(reverse('skills-directory'))

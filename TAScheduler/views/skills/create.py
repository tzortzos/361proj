from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.models import Skill
from TAScheduler.ClassDesign.LoginUtility import LoginUtility, UserType
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AllItems


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

        new_skill = request.POST.get(key='new_skill', default='')

        # Do not try to create empty skills
        if new_skill == '':
            return redirect(reverse('skills-directory'))

        # TODO use SkillsUtility to create the new skill

        return redirect(reverse('skills-directory'))

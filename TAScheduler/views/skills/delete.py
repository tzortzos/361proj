from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.models import Skill
from TAScheduler.ClassDesign.LoginUtility import LoginUtility, UserType
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.ClassDesign.SkillsUtility import SkillsUtility, Skill


class SkillsDelete(View):

    def get(self, request: HttpRequest, skill_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('index'),
            Message('You do not have permission to edit skills', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        if not SkillsUtility.delete_skill(skill_id):
            MessageQueue.push(
                request.session,
                Message(
                    'Cannot delete nonexistent skill',
                    Message.Type.ERROR,
                )
            )

        return redirect(reverse('skills-directory'))

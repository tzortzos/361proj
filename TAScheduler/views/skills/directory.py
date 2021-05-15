from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.models import Skill
from TAScheduler.ClassDesign.LoginUtility import LoginUtility, UserType
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AllItems


class SkillsDirectory(View):

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('index'),
            Message('You do not have permission to edit skills', Message.Type.ERROR)
        )

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/skills.html', {
            'self': user,
            'navbar_items': AllItems.for_type(user.type).without(AllItems.SKILLS).iter(),
            'message': MessageQueue.drain(request.session),

            'skills': list(Skill.objects.order_by('name').all()),
        })
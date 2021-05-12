from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.models import Skill
from TAScheduler.ClassDesign.LoginUtility import LoginUtility, UserType
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AllItems


class SkillsDelete(View):

    def get(self, request: HttpRequest, skill_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        return redirect(reverse('skills-directory'))

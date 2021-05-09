from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.models import Skill
from TAScheduler.ClassDesign.LoginUtility import LoginUtility, UserType
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AdminItems


class SkillsCreate(View):

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        return redirect(reverse('skills-directory'))

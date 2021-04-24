from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AdminItems

from TAScheduler.models import CourseSection, Course, User, UserType


class SectionsEdit(View):
    def get(self, request: HttpRequest, section_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        section = CourseSection.objects.all()[0]

        return render(request, 'pages/sections/edit_create.html', {
            'self': user,

            'section': section,
            'courses': list(Course.objects.all()),
            'professors': list(User.objects.filter(type=UserType.PROF)),
            'tas': list(User.objects.filter(type=UserType.TA)),
        })

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        pass

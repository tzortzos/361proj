from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.CourseAPI import Course, CourseAPI
from TAScheduler.ClassDesign.CourseSectionAPI import CourseSection, CourseSectionAPI
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.errors import SectionError
from TAScheduler.models import User, UserType, Course


class SectionsDirectory(View):
    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/sections/directory.html', {
            'self': user,
            'navbar_items': AdminItems.SECTIONS.items_iterable_except(),
            'messages': MessageQueue.drain(request.session),

            'sections': list(CourseSection.objects.all()),
        })
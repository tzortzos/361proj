from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union, Iterable

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.ClassDesign.CourseAPI import CourseAPI
from TAScheduler.models import Course

class CoursesDirectory(View):

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        courses: List[Course] = list(Course.objects.all())

        return render(request, 'pages/courses/directory.html', {
            'self': user,
            'navbar_items': AdminItems.COURSES.items_iterable_except(),
            'messages': MessageQueue.drain(request.session),

            'courses': courses,
        })

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union, Optional
from string import digits

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems

class CoursesCreate(View):

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('courses-directory'),
            Message(
                'You do not have permission to delete courses',
                Message.Type.ERROR
            ),
        )

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/courses/edit_create.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(),
        })

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('courses-directory'),
            Message(
                'You do not have permission to delete courses',
                Message.Type.ERROR
            ),
        )

        if type(user) is HttpResponseRedirect:
            return user

        course_code: Optional[str] = request.POST.get('course_code', None)
        course_name: Optional[str] = request.POST.get('course_name', None)

        if course_code is None or (a not in set(digits) for a in course_code):
            return render(request, 'pages/courses/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),
                'messages': MessageQueue.drain(),

                # TODO add error
            })

        # TODO check name



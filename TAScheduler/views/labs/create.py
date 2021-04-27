from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType, User, UserAPI
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.models import CourseSection
from TAScheduler.viewsupport.errors import LabError
from TAScheduler.ClassDesign.LabSectionAPI import LabSectionAPI, LabSection
from TAScheduler.ClassDesign.CourseSectionAPI import CourseSectionAPI

class LabsCreate(View):

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('labs-directory')),
            Message(
                'You do not have permission to create lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/labs/edit_create.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(request.session),

            'sections': CourseSection.objects.all(),
            'tas': User.objects.filter(type=UserType.TA),
        })

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('labs-directory')),
            Message(
                'You do not have permission to create lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        section_id = request.POST.get('section_id', None)
        lab_code = request.POST.get('lab_code', None)
        ta_id = request.POST.get('ta_id', None)
        lab_day = request.POST.get('lab_days', '')
        lab_time = request.POST.get('lab_time', '')

        if section_id is None:
            return render(request, 'pages/labs/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),
                'messages': MessageQueue.drain(request.session),

                'sections': CourseSection.objects.all(),
                'tas': User.objects.filter(type=UserType.TA),

                'error': LabError('You must pick a section for this lab', LabError.Place.SECTION),
            })

        if lab_code is None or len(lab_code) != 3:
            return render(request, 'pages/labs/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),
                'messages': MessageQueue.drain(request.session),

                'sections': CourseSection.objects.all(),
                'tas': User.objects.filter(type=UserType.TA),

                'error': LabError('You must provide a 3 digit lab code', LabError.Place.CODE),
            })

        section = CourseSectionAPI.get_course_section_by_course_id(section_id)

        if section is None:
            return render(request, 'pages/labs/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),
                'messages': MessageQueue.drain(request.session),

                'sections': CourseSection.objects.all(),
                'tas': User.objects.filter(type=UserType.TA),

                'error': LabError('You must pick a section for this lab', LabError.Place.SECTION),
            })

        if ta_id is not None:
            ta_id = UserAPI.get_user_by_user_id(ta_id)

        lab_id = LabSectionAPI.create_lab_section(lab_code, section, lab_day, lab_time, ta_id)

        return redirect(reverse('labs-view', args=[lab_id]))


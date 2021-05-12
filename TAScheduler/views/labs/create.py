from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union
from string import digits

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType, User, UserAPI
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.models import Section
from TAScheduler.viewsupport.errors import LabEditPlace, LabEditError
from TAScheduler.ClassDesign.LabAPI import LabAPI, Lab
from TAScheduler.ClassDesign.SectionAPI import SectionAPI

from more_itertools import ilen

class LabsCreate(View):

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('labs-directory')),
            Message(
                'You do not have permission to create new lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/labs/edit_create.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(request.session),

            'sections': Section.objects.all(),
            'tas': User.objects.filter(type=UserType.TA),
        })

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('labs-directory')),
            Message(
                'You do not have permission to create new lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        section_id = request.POST.get('section_id', None)
        lab_code = request.POST.get('lab_code', '')
        ta_id = request.POST.get('ta_id', None)
        lab_day = request.POST.get('lab_day', '')
        lab_time = request.POST.get('lab_time', '')

        def render_error(error: LabEditError):
            return render(request, 'pages/labs/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),
                'messages': MessageQueue.drain(request.session),

                'sections': Section.objects.all(),
                'tas': User.objects.filter(type=UserType.TA),

                'error': error,
            })

        if section_id is None:
            return render_error(LabEditError('You must pick a section for this lab', LabEditPlace.SECTION))

        non_digits = ilen((a for a in lab_code if a not in set(digits)))

        if lab_code is None or len(lab_code) != 3 or non_digits > 0:
            return render_error(LabEditError('You must provide a 3 digit lab code', LabEditPlace.CODE))

        section = SectionAPI.get_by_id(section_id)

        if section is None:
            return render_error(LabEditError('You must pick a section for this lab', LabEditPlace.SECTION))

        if ta_id is not None:
            ta_id = UserAPI.get_user_by_user_id(ta_id)

        lab_id = LabAPI.create_lab_section(lab_code, section, lab_day, lab_time, ta_id)

        return redirect(reverse('labs-view', args=[lab_id]))


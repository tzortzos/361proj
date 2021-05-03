from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union
from string import digits
from more_itertools import ilen

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType, User, UserAPI
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.ClassDesign.LabAPI import LabAPI
from TAScheduler.ClassDesign.SectionAPI import Section, SectionAPI
from TAScheduler.viewsupport.errors import LabEditError, LabEditPlace

class LabsEdit(View):
    def get(self, request: HttpRequest, lab_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN, UserType.PROF],
            reverse('labs-directory'),
            Message(
                'You do not have permission to edit lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        lab = LabAPI.get_by_id(lab_id)

        if lab is None:
            MessageQueue.push(request.session, Message(
                f'No such lab section with id {lab_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('labs-directory'))

        return render(request, 'pages/labs/edit_create.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(request.session),

            'edit': lab,

            'sections': Section.objects.all(),
            'tas': User.objects.filter(type=UserType.TA),
        })

    def post(self, request: HttpRequest, lab_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN, UserType.PROF],
            reverse('labs-directory'),
            Message(
                'You do not have permission to edit lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        lab = LabAPI.get_by_id(lab_id)

        if lab is None:
            MessageQueue.push(request.session, Message(
                f'No such lab section with id {lab_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('labs-directory'))

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
            return render_error(LabEditError('You cannot remove the 3 digit lab code', LabEditPlace.SECTION))

        non_digits = ilen((a for a in lab_code if a not in set(digits)))

        if lab_code is None or len(lab_code) != 3 or non_digits > 0:
            return render_error(LabEditError('You cannot remove the 3 digit lab code', LabEditPlace.CODE))

        lab.code = lab_code

        section = SectionAPI.get_by_id(section_id)

        if section is None:
            return render_error(LabEditError('You cannot remove a section from this lab', LabEditPlace.SECTION))

        lab.section = section

        if ta_id is not None and ta_id != -1:
            lab.ta = UserAPI.get_user_by_user_id(ta_id)

        if ta_id is not None and ta_id == -1:
            lab.ta = None

        lab.day = lab_day
        lab.time = lab_time

        lab.save()

        return redirect(reverse('labs-directory'))

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.ClassDesign.LabSectionAPI import LabSectionAPI

class LabsDelete(View):

    def get(self, request: HttpRequest, lab_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('labs-directory'),
            Message(
                'You do not have permission to delete lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        lab = LabSectionAPI.get_lab_section_by_lab_id(lab_id)

        if lab is None:
            MessageQueue.push(request.session, Message(
                f'No such lab section with id {lab_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('labs-directory'))

        return render(request, 'pages/labs/view.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(request.session),

            'lab': lab,
        })

    def post(self, request: HttpRequest, lab_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('labs-directory'),
            Message(
                'You do not have permission to delete lab sections',
                Message.Type.ERROR,
            )
        )

        if type(user) is HttpResponseRedirect:
            return user

        lab = LabSectionAPI.get_lab_section_by_lab_id(lab_id)

        if lab is None:
            MessageQueue.push(request.session, Message(
                f'No such lab section with id {lab_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('labs-directory'))

        LabSectionAPI.delete_lab_section(lab_id)

        MessageQueue.push(request.session, Message('Successfully deleted lab section'))

        return redirect(reverse('labs-directory'))

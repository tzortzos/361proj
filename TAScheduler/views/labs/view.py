from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.ClassDesign.LabAPI import LabAPI

class LabsView(View):

    def get(self, request: HttpRequest, lab_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        lab = LabAPI.get_lab_section_by_lab_id(lab_id)

        if lab is None:
            MessageQueue.push(request.session, Message(
                f'No such lab section with id {lab_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('labs-directory'))

        return render(request, 'pages/labs/view.html', {
            'self': user,
            'navbar_items': AllItems.for_type(user.type).iter(),
            'messages': MessageQueue.drain(request.session),

            'lab': lab,
        })

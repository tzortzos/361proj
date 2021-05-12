from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.ClassDesign.LabAPI import LabAPI, Lab

class LabsDirectory(View):

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        labs = Lab.objects.all()

        return render(request, 'pages/labs/directory.html', {
            'self': user,
            'navbar_items': AllItems.for_type(user.type).without(AllItems.LABS).iter(),
            'messages': MessageQueue.drain(request.session),

            'labs': labs,
        })

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.ClassDesign.LabAPI import LabAPI, Lab
from TAScheduler.ClassDesign.SectionAPI import SectionAPI, Section
from TAScheduler.ClassDesign.UserAPI import User

def get(request: HttpRequest, user: User) -> HttpResponse:
    return render(request, 'pages/dashboards/ta.html', {
        "self": user,
        "messages": MessageQueue.drain(request.session),
        "navbar_items": AdminItems.HOME.items_iterable_except(),

        "message_count": 17,
        "sections": Section.objects.all(),
        "labs": Lab.objects.all()
    })
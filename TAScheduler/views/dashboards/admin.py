from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union
from django.db.models import Count

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.ClassDesign.CourseAPI import Course, CourseAPI
from TAScheduler.ClassDesign.UserAPI import User

def get(request: HttpRequest, user: User) -> HttpResponse:
    return render(request, 'pages/dashboards/prof.html', {
        "self": user,
        "messages": MessageQueue.drain(request.session),
        "navbar_items": AllItems.for_type(user.type).without(AllItems.HOME).iter(),

        "message_count": 17,

        unassigned_percent = 100.0 * Count(Course.objects.filter(""))/Course.objects.count(),
        assigned_percent = 100.0 * Count(Course.objects.filter())/Course.objects.count(),

        "percent_of_classes_assigned": unnassigned_precent
    })
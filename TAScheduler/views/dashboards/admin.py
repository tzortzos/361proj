from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union
from django.db.models import Count

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.ClassDesign.SectionAPI import SectionAPI, Section
from TAScheduler.ClassDesign.LabAPI import LabAPI, Lab
from TAScheduler.ClassDesign.UserAPI import User, UserType


def get(request: HttpRequest, user: User) -> HttpResponse:
    num_sections = Section.objects.count()

    if num_sections > 0:
        section_unassigned_percent = 100.0 * Section.objects.filter(prof=None).count() / num_sections
        section_assigned_percent = 100.0 - section_unassigned_percent
    else:
        section_assigned_percent = 0
        section_unassigned_percent = 100

    num_labs = Lab.objects.count()

    if num_labs > 0:
        lab_unassigned_percent = 100.0 * Lab.objects.filter(ta=None).count() / num_labs
        lab_assigned_percent = 100.0 - lab_unassigned_percent
    else:
        lab_assigned_percent = 0
        lab_unassigned_percent = 100

    num_tas = User.objects.filter(type=UserType.TA).count()

    if num_tas > 0:
        ta_assigned_percent = 100.0 * \
                              len(list(filter(
                                  lambda ta: ta.lab_set.count() > 0,
                                  User.objects.filter(type=UserType.TA)
                              )))\
                              / num_tas
    else:
        ta_assigned_percent = 0

    ta_unassigned_percent = 100.0 - ta_assigned_percent

    num_prof = User.objects.filter(type=UserType.PROF).count()

    if num_prof > 0:
        prof_assigned_percent = 100.0 * \
                              len(list(filter(
                                  lambda prof: prof.section_set.count() > 0,
                                  User.objects.filter(type=UserType.PROF)
                              ))) \
                              / num_prof
    else:
        prof_assigned_percent = 0

    prof_unassigned_percent = 100.0 - prof_assigned_percent

    return render(request, 'pages/dashboards/admin.html', {
        "self": user,
        "messages": MessageQueue.drain(request.session),
        "navbar_items": AllItems.for_type(user.type).without(AllItems.HOME).iter(),

        "message_count": 17,

        # Section Percentage
        "num_sections": num_sections,
        "section_assigned_percent": section_assigned_percent,
        "section_unassigned_percent": section_unassigned_percent,

        # Lab Percentage
        "num_labs": num_labs,
        "lab_assigned_percent": lab_unassigned_percent,
        "lab_unassigned_percent": lab_assigned_percent,

        # TA's Percentage
        "num_tas": num_tas,
        "ta_assigned_percent": ta_assigned_percent,
        "ta_unassigned_percent": ta_unassigned_percent,

        # Prof's Percentage
        "num_prof": num_prof,
        "prof_assigned_percent": prof_assigned_percent,
        "prof_unassigned_percent": prof_unassigned_percent
    })
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from typing import Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.SectionAPI import Section
from TAScheduler.viewsupport.message import MessageQueue
from TAScheduler.viewsupport.navbar import AllItems


class SectionsDirectory(View):
    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/sections/directory.html', {
            'self': user,
            'navbar_items': AllItems.for_type(user.type).without(AllItems.SECTIONS).iter(),
            'messages': MessageQueue.drain(request.session),

            'sections': list(Section.objects.all()),
        })
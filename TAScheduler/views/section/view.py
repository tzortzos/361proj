from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.SectionAPI import Section, SectionAPI
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems


class SectionsView(View):
    def get(self, request: HttpRequest, section_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        section = SectionAPI.get_by_id(section_id)

        if section is None:
            MessageQueue.push(request.session, Message(
                f'No Course Section exists with the id {section_id}',
                Message.Type.ERROR,
            ))
            return redirect(reverse('sections-directory'))

        return render(request, 'pages/sections/view.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(request.session),

            'section': section,
        })

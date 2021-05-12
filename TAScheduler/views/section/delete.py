from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

# from TAScheduler.ClassDesign.CourseSectionAPI import
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AllItems

from TAScheduler.ClassDesign.SectionAPI import SectionAPI


class SectionsDelete(View):

    def get(self, request: HttpRequest, section_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('sections-directory')),
            Message('You do not have permission to delete Course Sections', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        section = SectionAPI.get_by_id(section_id)

        if section is None:
            MessageQueue.push(request.session, Message(
                f'No Course Section exists with the id {section_id}',
                Message.Type.ERROR,
            ))
            return redirect(reverse('sections-directory'))

        return render(request, 'pages/sections/delete.html', {
            'self': user,
            'navbar_items': AllItems.for_type(user.type).iter(),
            'messages': MessageQueue.drain(request.session),

            'to_delete': section,
        })


    def post(self, request: HttpRequest, section_id: int) -> HttpResponseRedirect:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('sections-directory')),
            Message('You do not have permission to delete Course Sections', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        section = SectionAPI.get_by_id(section_id)
        # NOTE It might be nice for delete to return information about the deleted object
        # (or the deleted object itself?)
        success = SectionAPI.delete_by_id(section_id)

        if success:
            MessageQueue.push(request.session, Message(
                f'Successfully deleted Course Section {section.code}'
                f' for course {section.course.code} {section.course.name}'
            ))
            return redirect(reverse('sections-directory'))
        else:
            MessageQueue.push(request.session, Message(
                f'No Course Section exists with the id {section_id}',
                Message.Type.ERROR,
            ))
            return redirect(reverse('sections-directory'))

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserType
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.ClassDesign.CourseAPI import Course, CourseAPI

class CoursesView(View):

    def get(self, request: HttpRequest, course_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        course = CourseAPI.get_course_by_course_id(course_id)

        if course is None:
            MessageQueue.push(request.session, Message(
                f'No such course with id {course_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('courses-directory'))

        return render(request, 'pages/courses/view.html', {
            'self': user,
            'navbar_items': AllItems.for_type(user.type).iter(),
            'messages': MessageQueue.drain(request.session),

            'course': course,
        })

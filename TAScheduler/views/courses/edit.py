from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union, Optional
from string import digits

from TAScheduler.ClassDesign.LoginUtility import LoginUtility, UserType
from TAScheduler.ClassDesign.CourseAPI import CourseAPI, Course
from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.errors import CourseEditError, CourseEditPlace

class CoursesEdit(View):

    def get(self, request: HttpRequest, course_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('courses-directory'),
            Message(
                'You do not have permission to delete courses',
                Message.Type.ERROR
            ),
        )

        if type(user) is HttpResponseRedirect:
            return user

        course = CourseAPI.get_course_by_course_id(course_id)

        if course is None:
            MessageQueue.push(request.session, Message(
                f'No course with id {course_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('courses-directory'))

        return render(request, 'pages/courses/edit_create.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(request.session),

            'edit': course
        })

    def post(self, request: HttpRequest, course_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('courses-directory'),
            Message(
                'You do not have permission to delete courses',
                Message.Type.ERROR
            ),
        )

        if type(user) is HttpResponseRedirect:
            return user

        course: Optional[Course] = CourseAPI.get_course_by_course_id(course_id)

        if course is None:
            MessageQueue.push(request.session, Message(
                f'No course with id {course_id} exists',
                Message.Type.ERROR,
            ))
            return redirect(reverse('courses-directory'))

        course_code: Optional[str] = request.POST.get('course_code', None)
        course_name: Optional[str] = request.POST.get('course_name', None)

        def render_error(error: CourseEditError):
            return render(request, 'pages/courses/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),
                'messages': MessageQueue.drain(request.session),

                'edit': course,

                'error': error
            })

        if course_code is None:
            return render_error(CourseEditError(
                    'You cannot remove a course code',
                    CourseEditPlace.CODE
                ))

        if len(course_code) != 3:
            return render_error(CourseEditError(
                    'A course code must be exactly 3 digits',
                    CourseEditPlace.CODE
                ))

        if course_name is None:
            return render_error(CourseEditError(
                    'You cannot remove the course name',
                    CourseEditPlace.NAME,
                ))

        # TODO replace with CourseAPI edit method later
        course.name = course_name
        course.code = course_code
        course.save()

        return redirect(reverse('courses-view', args=[course.id]))

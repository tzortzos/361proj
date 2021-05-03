from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import User, UserType, UserAPI
from TAScheduler.ClassDesign.CourseAPI import Course, CourseAPI
from TAScheduler.ClassDesign.SectionAPI import Section, SectionAPI
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.errors import SectionEditPlace, SectionEditError
from TAScheduler.models import User, UserType, Course


class SectionsCreate(View):
    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('sections-directory'),
            Message('You do not have permission to create Course Sections', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/sections/edit_create.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),

            'courses': Course.objects.all(),
            'professors': User.objects.filter(type=UserType.PROF),
            'tas': User.objects.filter(type=UserType.TA),
        })

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            reverse('sections-directory'),
            Message('You do not have permission to create Course Sections', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        # TODO create a helper function for views getting a set of variables out of a context
        section_code = request.POST.get('section_code', None)
        course_id = request.POST.get('course_id', -1)
        lecture_days = ''.join(request.POST.getlist('lecture_days', []))
        lecture_time = request.POST.get('lecture_time', None)
        instructor_id = request.POST.get('professor_id', None)
        ta_ids = request.POST.getlist('ta_ids', [])

        course = CourseAPI.get_course_by_course_id(course_id)

        if course is None:
            return render(request, 'pages/sections/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),

                'courses': Course.objects.all(),
                'professors': User.objects.filter(type=UserType.PROF),
                'tas': User.objects.filter(type=UserType.TA),

                'error': SectionEditError('You must select a course for this section', SectionEditPlace.COURSE),
            })

        if section_code is None:
            return render(request, 'pages/sections/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),

                'courses': Course.objects.all(),
                'professors': User.objects.filter(type=UserType.PROF),
                'tas': User.objects.filter(type=UserType.TA),

                'error': SectionEditError('You must input a 3 digit section code', SectionEditPlace.CODE),
            })


        try:
            # NOTE it would be really nice if this could catch the integrity error and return an unsaved version of the
            #      database object in the case that it could not be saved, that way we could re-fill the fields with
            #      the relevant information in this case.
            section_id: int = SectionAPI.create_course_section(section_code, course)
        except IntegrityError:
            return render(request, 'pages/sections/edit_create.html', {
                'self': user,
                'navbar_items': AdminItems.items_iterable(),

                'courses': Course.objects.all(),
                'professors': User.objects.filter(type=UserType.PROF),
                'tas': User.objects.filter(type=UserType.TA),

                'error': SectionEditError('A section already exists for this course with that code', SectionEditPlace.CODE),
            })


        # TODO Replace with CourseSectionAPI methods when complete
        section = Section.objects.get(id=section_id)

        if section is None:
            raise ValueError('Could not create section')

        if len(lecture_days) > 0:
            section.days = lecture_days

        if lecture_time is not None:
            section.time = lecture_time

        if instructor_id is not None:
            instructor = UserAPI.get_user_by_user_id(instructor_id)

            if instructor is not None:
                section.prof = instructor

        tas = list(filter(lambda a: a is not None, map(UserAPI.get_user_by_user_id, ta_ids)))

        for ta in tas:
            section.tas.add(ta)

        section.save()

        return redirect(reverse('sections-view', args=(section_id,)))

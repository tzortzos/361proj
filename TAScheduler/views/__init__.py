from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import List

from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.message import MessageQueue

# Reexport Views from Submodules
from TAScheduler.views.login import Login
from TAScheduler.views.logout import Logout

from TAScheduler.views.users.edit import UserEdit
from TAScheduler.views.users.create import UserCreate
from TAScheduler.views.users.delete import UserDelete
from TAScheduler.views.users.directory import UserDirectory
from TAScheduler.views.users.view import UserView

from TAScheduler.views.section.directory import SectionsDirectory
from TAScheduler.views.section.create import SectionsCreate
from TAScheduler.views.section.edit import SectionsEdit
from TAScheduler.views.section.view import SectionsView
from TAScheduler.views.section.delete import SectionsDelete

from TAScheduler.views.labs.create import LabsCreate
from TAScheduler.views.labs.delete import LabsDelete
from TAScheduler.views.labs.directory import LabsDirectory
from TAScheduler.views.labs.edit import LabsEdit
from TAScheduler.views.labs.view import LabsView

from TAScheduler.views.courses.create import CoursesCreate
from TAScheduler.views.courses.delete import CoursesDelete
from TAScheduler.views.courses.directory import CoursesDirectory
from TAScheduler.views.courses.edit import CoursesEdit
from TAScheduler.views.courses.view import CoursesView


class Index(View):
    def get(self, request: HttpRequest):
        return render(request, 'pages/index.html', context={
            'navbar_items': AdminItems.HOME.items_iterable_except(),
            'messages': MessageQueue.drain(request.session),
        })


class CourseEdit(View):
    def get(self, request):
        return render(request, 'pages/create_course.html', {
            'navbar_items': AdminItems.items_iterable(),
        })

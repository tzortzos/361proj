from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import List

from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.message import Message

# Reexport Views from Submodules
from TAScheduler.views.login import Login
from TAScheduler.views.users.edit import UserEdit
from TAScheduler.views.users.create import UserCreate


class Index(View):

    def get(self, request: HttpRequest, messages: List[Message] = []):
        return render(request, 'pages/example.html', context={
            'navbar_items': AdminItems.HOME.items_iterable_except(),
            'user_name': 'Josiah Hilden',
            'messages': messages,
        })

    def post(self, request):
        return render(request, 'pages/index.html')


class CourseEdit(View):
    def get(self, request):
        return render(request, 'pages/create_course.html', {
            'navbar_items': AdminItems.items_iterable(),
        })

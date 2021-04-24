
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType, User
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AdminItems


class UserDirectory(View):
    def get(self, request: HttpRequest):
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        return render(request, 'pages/user_directory.html', {
            'self': user,
            'navbar_items': AdminItems.USERS.items_iterable_except(),  # TODO change for other user types
            'messages': MessageQueue.drain(request.session),

            'users': User.objects.iterator(),
        })

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse

from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserAPI


class UserView(View):

    def get(self, request: HttpRequest, user_id: int):
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        to_display = UserAPI.get_user_by_user_id(user_id)

        if to_display is None:
            MessageQueue.push(request.session, Message(f'No user with id {user_id} exists', Message.Type.ERROR))
            return redirect(reverse('index'))

        return render(request, 'pages/users/view.html', context={
            'navbar_items': AdminItems.items_iterable(),
            'messages': MessageQueue.drain(request.session),
            'self': user,
            'user': to_display,
        })

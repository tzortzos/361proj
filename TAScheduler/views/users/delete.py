from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AllItems


class UserDelete(View):
    """
    Represents the page which confirms the deletion of a user from the database. Redirects non admins to the index.
    """

    def get(self, request: HttpRequest, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('users-directory')),
            Message('You do not have permission to delete users', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        # We have a user which we know to be an admin, so it is safe to show them the page
        to_delete = UserAPI.get_user_by_user_id(user_id)

        if to_delete is None:
            MessageQueue.push(request.session, Message(f'No user with id {user_id} exists.', Message.Type.ERROR))
            return redirect(reverse('users-directory'))

        return render(request, 'pages/users/delete.html', {
            'self': user,
            'messages': MessageQueue.drain(request.session),
            'navbar_items': AllItems.for_type(user.type).iter(),
            'to_delete': to_delete,
        })

    def post(self, request: HttpRequest, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('users-directory')),
            Message('You do not have permission to delete users', Message.Type.ERROR),
        )

        if type(user) is HttpResponseRedirect:
            return user

        to_delete = UserAPI.get_user_by_user_id(user_id)

        if to_delete is None:
            MessageQueue.push(request.session, Message(f'No user with id {user_id} exists', Message.Type.ERROR))
            return redirect(reverse('users-directory'))

        UserAPI.delete_user(user_id)

        MessageQueue.push(request.session, Message(f'Successfully deleted user {to_delete.username}'))
        return redirect(reverse('users-directory'))

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import Message
from TAScheduler.viewsupport.navbar import AdminItems


class UserDelete(View):
    """
    Represents the page which confirms the deletion of a user from the database. Redirects non admins to the index.
    """

    def get(self, request: HttpRequest, user_id: int, messages: List[Message] = []) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('index', args=(
                [Message('You do not have permission to delete users', Message.Type.ERROR)] + messages,
            )))
        )

        if type(user) is HttpResponseRedirect:
            return user

        # We have a user which we know to be an admin, so it is safe to show them the page
        to_delete = UserAPI.get_user_by_user_id(user_id)

        if to_delete is None:
            return redirect(reverse('users-directory', args=(
                [Message(f'No user with id {user_id} exists.', Message.Type.ERROR)] + messages,
            )))

        return render(request, 'pages/user_delete.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'to_delete': to_delete,
        })

    def post(self, request: HttpRequest, user_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
        user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
            redirect(reverse('index', args=(
                [Message('You do not have permission to delete users', Message.Type.ERROR)],
            )))
        )

        if type(user) is HttpResponseRedirect:
            return user

        # We have an admin user so it is safe to delete
        to_delete = UserAPI.get_user_by_user_id(user_id)

        if to_delete is None:
            return redirect(reverse('users-directory', args=(
                [Message(f'No user with id {user_id} exists', Message.Type.ERROR)],
            )))

        UserAPI.delete_user(to_delete)

        return redirect(reverse('users-directory', args=(
            [Message(f'Successfully delete user {to_delete.univ_id}')],
        )))

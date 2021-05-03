from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Union
from typing import List, Optional

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.errors import UserEditError, UserEditPlace
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.ClassDesign.Util import Util


class UserCreate(View):
    """
    Represents the creation of a new user object in the database.
    Uses the create_user page template in the create configuration.
    """

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        maybe_user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
        )
        if type(maybe_user) is HttpResponseRedirect:
            return maybe_user

        tmp_pass = LoginUtility.generate_tmp_password()

        return render(request, 'pages/users/edit_create.html', {
            'self': maybe_user,
            'navbar_items': AdminItems.items_iterable(),
            'new_user_pass': tmp_pass,
            'messages': MessageQueue.drain(request.session),
        })

    def post(self, request: HttpRequest):
        maybe_user = LoginUtility.get_user_and_validate_by_user_id(
            request.session,
            [UserType.ADMIN],
        )
        if type(maybe_user) is HttpResponseRedirect:
            return maybe_user

        new_pass: Optional[str] = request.POST.get('new_password', None)
        username: Optional[str] = request.POST.get('univ_id', None)

        user_type: Optional[UserType] = Util[str, UserType].optional_map(
            UserType.try_from_str,
            request.POST.get('user_type', None),
        )

        if new_pass is None or len(new_pass) < 8:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('Password must be at least 8 characters in length', UserEditPlace.PASSWORD),
                'new_user_pass': LoginUtility.generate_tmp_password(),
            })

        if username is None or len(username) == 0:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('You must provide a university id', UserEditPlace.USERNAME),
                'new_user_pass': new_pass,
            })
        elif len(username) > 20:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('A university id may not be longer than 20 characters', UserEditPlace.USERNAME),
                'new_user_pass': new_pass,
            })
        elif len(''.join(filter(lambda c: c == ' ', iter(username)))) > 0:
            print(f'found spaces in "{username}"')
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('A username may not have spaces', UserEditPlace.USERNAME),
                'new_user_pass': new_pass,
            })
        elif len(''.join(filter(lambda c: c == '@', username))) > 0:
            print(f'found @ sign in in "{username}"')
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('You only need to put in the first part of a university email', UserEditPlace.USERNAME),
                'new_user_pass': new_pass,
            })

        if user_type is None:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('You must provide a user type', UserEditPlace.TYPE),
                'new_user_pass': new_pass,
            })

        l_name = request.POST.get('l_name', None)
        f_name = request.POST.get('f_name', None)
        phone = request.POST.get('phone', None)

        user_id = UserAPI.create_user(user_type, username, new_pass)
        UserAPI.update_user(UserAPI.get_user_by_user_id(user_id), l_name, f_name, phone)

        return redirect(reverse('users-directory'))









from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Union
from typing import List

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.errors import PageError, UserEditError
from TAScheduler.viewsupport.message import Message, MessageQueue


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

        try:
            new_pass = str(request.POST['new_password'])
        except KeyError:
            new_pass = None

        if new_pass is None or len(new_pass) < 8:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('Password must be at least 8 characters in length', UserEditError.Place.PASSWORD),
                'new_user_pass': LoginUtility.generate_tmp_password(),
            })

        try:
            univ_id = str(request.POST['univ_id'])
        except KeyError:
            univ_id = None

        if univ_id is None or len(univ_id) == 0:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('You must provide a university id', UserEditError.Place.USERNAME),
                'new_user_pass': new_pass,
            })
        elif len(univ_id) > 20:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('A university id may not be longer than 20 characters', UserEditError.Place.USERNAME),
                'new_user_pass': new_pass,
            })
        elif len(''.join(filter(lambda c: c == ' ', iter(univ_id)))) > 0:
            print(f'found spaces in "{univ_id}"')
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('A username may not have spaces', UserEditError.Place.USERNAME),
                'new_user_pass': new_pass,
            })
        elif len(''.join(filter(lambda c: c == '@', univ_id))) > 0:
            print(f'found @ sign in in "{univ_id}"')
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('You only need to put in the first part of a university email', UserEditError.Place.USERNAME),
                'new_user_pass': new_pass,
            })

        # TODO: Check univ id for special characters.

        try:
            user_type = str(request.POST['user_type'])
        except:
            user_type = None

        if user_type is None or user_type not in ['A', 'P', 'T']:
            return render(request, 'pages/users/edit_create.html', {
                'self': maybe_user,
                'error': UserEditError('You must provide a user type', UserEditError.Place.TYPE),
                'new_user_pass': new_pass,
            })

        try:
            l_name = str(request.POST['l_name'])
        except KeyError:
            l_name = None

        try:
            f_name = request.POST['f_name']
        except KeyError:
            f_name = None

        try:
            phone = request.POST['phone']

        except KeyError:
            phone = None

        user_id = UserAPI.create_user(user_type, univ_id, new_pass)
        UserAPI.update_user(UserAPI.get_user_by_user_id(user_id), l_name, f_name, phone)

        return redirect(reverse('users-directory'))









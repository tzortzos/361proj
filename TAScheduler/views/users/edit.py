from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from typing import Dict

from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.errors import UserEditError, PageError
from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.navbar import AdminItems


# Obviously just a stub, needed to make login acceptance tests pass.
class UserEdit(View):
    """
    Represents the user edit page, which will only be visible if editing self or logged in user is admin.
    """

    def get(self, request: HttpRequest, user_id: int):
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        to_edit = UserAPI.get_user_by_user_id(user_id)

        if to_edit is None:
            MessageQueue.push(request.session, Message('No user with id {user_id} exists.', Message.Type.ERROR))
            return redirect(reverse('users-directory'))

        if to_edit.user_id != user.user_id and UserAPI.check_user_type(user) != UserType.ADMIN:
            MessageQueue.push(request.session, Message(f'You are not allowed to edit other users.', Message.Type.ERROR))
            return redirect(reverse('index'))

        return render(request, 'pages/create_user.html', {
            'navbar_items': AdminItems.items_iterable(),  # TODO Change based on user type later
            'self': user,
            'edit': to_edit,
        })

    def post(self, request: HttpRequest, user_id: int):
        user = LoginUtility.get_user_and_validate_by_user_id(request.session)

        if type(user) is HttpResponseRedirect:
            return user

        to_edit = UserAPI.get_user_by_user_id(user_id)

        if to_edit is None:
            MessageQueue.push(request.session, Message('No user with id {user_id} exists.', Message.Type.ERROR))
            return redirect(reverse('users-directory'))

        if to_edit.user_id != user.user_id and UserAPI.check_user_type(user) != UserType.ADMIN:
            MessageQueue.push(request.session, Message(f'You are not allowed to edit other users.', Message.Type.ERROR))
            return redirect(reverse('index'))

        # Get all the possible values from the context
        fields: Dict[str, str] = {}
        try:
            fields['univ_id'] = str(request.POST['univ_id'])
        except KeyError:
            fields['univ_id'] = None

        try:
            fields['user_type'] = str(request.POST['user_type'])
        except KeyError:
            fields['user_type'] = None

        try:
            fields['f_name'] = str(request.POST['f_name'])
        except KeyError:
            fields['f_name'] = None

        try:
            fields['l_name'] = str(request.POST['l_name'])
        except KeyError:
            fields['l_name'] = None

        try:
            fields['phone'] = str(request.POST['phone'])
        except KeyError:
            fields['phone'] = None

        try:
            fields['old_password'] = str(request.POST['old_password'])
        except KeyError:
            fields['old_password'] = None

        try:
            fields['new_password'] = str(request.POST['new_password'])
        except KeyError:
            fields['new_password'] = None

        # Check error cases
        if fields['new_password'] is not None and len(fields['new_password']) >= 8:
            # Attempting to change password
            if user.user_id != to_edit.user_id:
                # Admins may not change others' passwords
                MessageQueue.push(
                    request.session,
                    Message('You may not change other users password', Message.Type.ERROR)
                )
                return render(request, 'pages/create_user.html', {
                    'navbar_items': AdminItems.items_iterable(),
                    'self': user,
                    'edit': to_edit,
                })

            if fields['old_password'] is None or str(to_edit.password) != fields['old_password']:
                return render(request, 'pages/create_user.html', {
                    'navbar_items': AdminItems.items_iterable(),  # TODO change based on user type
                    'self': user,
                    'edit': to_edit,
                    'error': UserEditError('Incorrect password', UserEditError.Place.PASSWORD),
                })

            LoginUtility.update_password(to_edit, fields['new_password'])
            # Done changing password

        if fields['univ_id'] is None or len(fields['univ_id']) == 0:
            return render(request, 'pages/create_user.html', {
                'navbar_items': AdminItems.items_iterable(),  # TODO change based on user type
                'self': user,
                'edit': to_edit,
                'error': UserEditError('You can\'t remove a user\'s username.', UserEditError.Place.USERNAME),
            })

        if fields['univ_id'] != to_edit.user_id:
            if UserAPI.check_user_type(user) != UserType.ADMIN:
                return render(request, 'pages/create_user.html', {
                    'navbar_items': AdminItems.items_iterable(),  # TODO change based on user type
                    'self': user,
                    'edit': to_edit,
                    'error': UserEditError('You cannot change your own username', UserEditError.Place.USERNAME),
                })

            to_edit.univ_id = fields['univ_id']
            to_edit.save()

        UserAPI.update_user(to_edit, fields['l_name'], fields['f_name'], fields['phone'])

        return redirect(reverse('users-view', args=(to_edit.user_id,)))


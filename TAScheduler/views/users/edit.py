from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from typing import Dict, Optional

from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.errors import UserEditError, UserEditPlace
from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.navbar import AllItems
from TAScheduler.models import Skill

# Obviously just a stub, needed to make login acceptance tests pass.
class UserEdit(View):
    """
    Represents the user edit page, which will only be visible if editing self or logged in user is admin.
    """

    def get(self, request: HttpRequest, user_id: int):
        user = LoginUtility.get_user_and_validate_by_user_id(request.session, password_change_redirect=False)

        if type(user) is HttpResponseRedirect:
            return user

        to_edit = UserAPI.get_user_by_user_id(user_id)

        if to_edit is None:
            MessageQueue.push(request.session, Message('No user with id {user_id} exists.', Message.Type.ERROR))
            return redirect(reverse('users-directory'))

        if to_edit.id != user.id and UserAPI.check_user_type(user) != UserType.ADMIN:
            MessageQueue.push(request.session, Message('You are not allowed to edit other users.', Message.Type.ERROR))
            return redirect(reverse('index'))

        return render(request, 'pages/users/edit_create.html', {
            'navbar_items': AllItems.for_type(user.type).iter(),
            'self': user,
            'edit': to_edit,
        })

    def post(self, request: HttpRequest, user_id: int):
        user = LoginUtility.get_user_and_validate_by_user_id(request.session, password_change_redirect=False)

        if type(user) is HttpResponseRedirect:
            return user

        to_edit = UserAPI.get_user_by_user_id(user_id)

        if to_edit is None:
            MessageQueue.push(request.session, Message(f'No user with id {user_id} exists.', Message.Type.ERROR))
            return redirect(reverse('users-directory'))

        if to_edit.id != user.id and UserAPI.check_user_type(user) != UserType.ADMIN:
            MessageQueue.push(request.session, Message('You are not allowed to edit other users.', Message.Type.ERROR))
            return redirect(reverse('index'))

        # Get all the possible values from the context
        fields: Dict[str, Optional[str]] = {}
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

        def render_error(error: UserEditError):
            return render(request, 'pages/users/edit_create.html', {
                'navbar_items': AllItems.for_type(user.type).iter(),
                'self': user,
                'edit': to_edit,

                'skills': list(Skill.objects.all()),

                'error': error,
            })

        # Check error cases
        if fields['new_password'] is not None and len(fields['new_password']) > 0:
            # Attempting to change password
            if user.id != to_edit.id:
                # Admins may not change others' passwords
                MessageQueue.push(
                    request.session,
                    Message('You may not change another users password', Message.Type.ERROR)
                )
                return render(request, 'pages/users/edit_create.html', {
                    'navbar_items': AllItems.for_type(user.type).iter(),
                    'self': user,
                    'edit': to_edit,
                })

            if fields['old_password'] is None or str(to_edit.password) != fields['old_password']:
                return render_error(UserEditError('Incorrect password', UserEditPlace.PASSWORD))

            if len(fields['new_password']) < 8:
                return render_error(UserEditError('New Password needs to be 8 or more characters.', UserEditPlace.PASSWORD))

            LoginUtility.update_password(to_edit, fields['new_password'])
            MessageQueue.push(request.session, Message('Password Updated'))
            # Done changing password

        if fields['old_password'] is not None and\
                len(fields['old_password']) > 0 and\
                (fields['new_password'] is None or len(fields['new_password']) == 0):
            return render_error(UserEditError('New password can\'t be empty.', UserEditPlace.PASSWORD))

        if fields['univ_id'] is None or len(fields['univ_id']) == 0:
            return render_error(UserEditError('You can\'t remove a user\'s username.', UserEditPlace.USERNAME))

        if fields['univ_id'] != to_edit.username and to_edit != user:
            if UserAPI.check_user_type(user) != UserType.ADMIN:
                return render_error(UserEditError('You cannot change your own username', UserEditPlace.USERNAME))

            if len(fields['univ_id']) > 20:
                return render_error(UserEditError(
                        'A username may not be longer than 20 characters.',
                        UserEditPlace.USERNAME
                    ))

            to_edit.username = fields['univ_id']
            to_edit.save()

        if fields['phone'] is not None:
            # Extract only the digits from the supplied phone number
            fields['phone'] = ''.join(filter(lambda a: a.isdigit(), fields['phone']))

            print(f'Phone number extracted: ' + fields['phone'])

            if len(fields['phone']) > 0 and len(fields['phone']) != 10:
                return render_error(UserEditError(
                        'Phone number needs to be exactly 10 digits long.',
                        UserEditPlace.PHONE
                    ))

        UserAPI.update_user(to_edit, fields['l_name'], fields['f_name'], fields['phone'])

        if fields['l_name'] is not None or fields['f_name'] is not None or fields['phone'] is not None:
            MessageQueue.push(request.session, Message('Contact Information Updated'))

        if fields['user_type'] is not None:
            # Chane user type
            if UserAPI.check_user_type(user) != UserType.ADMIN:
                return render_error(UserEditError(
                        'Only admins may change user types',
                        UserEditPlace.TYPE
                    ))

            # to_edit.type = fields['user_type']

            if fields['user_type'] == 'A':
                to_edit.type = UserType.ADMIN
            elif fields['user_type'] == 'P':
                to_edit.type = UserType.PROF
            else:
                to_edit.type = UserType.TA

            to_edit.save()
            MessageQueue.push(request.session, Message(f'User {to_edit.username} is now a {to_edit.get_type_display()}'))

        return redirect(reverse('users-view', args=(to_edit.id,)))


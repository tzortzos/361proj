from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

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
        pass


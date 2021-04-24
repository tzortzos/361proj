import uuid
from typing import Union, Optional, List
from django.http import HttpResponseRedirect

from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.models import User
from TAScheduler.viewsupport.message import Message, MessageQueue
from django.shortcuts import redirect, reverse
from django.contrib.sessions.backends.base import SessionBase


class LoginUtility:

    @staticmethod
    def update_password(user: User, password: str):
        user.password = password
        user.tmp_password = False
        user.save()

    @staticmethod
    def generate_tmp_password() -> str:
        return str(uuid.uuid4())[:8]

    @staticmethod
    def get_user_and_validate_by_user_id(
            session: SessionBase,
            types: Optional[List[UserType]] = None,
            redirect_to: Optional[HttpResponseRedirect] = None,
            redirect_message: Optional[Message] = None,
            password_change_redirect: bool = True,
    ) -> Union[User, HttpResponseRedirect]:
        """
        Get a user from a request context and validate the user's type
        To ensure that the user has permission to look at this page at this time.
        If the user is redirected for being the incorrect type then `redirect_message` is added to their message queue.
        """

        try:
            user_id = session['user_id']
        except KeyError:
            user_id = None

        if user_id is None or type(user_id) is not int:
            MessageQueue.push(session, Message('You must log into the application before you can view that page'))
            return redirect(reverse('login'))

        user = UserAPI.get_user_by_user_id(user_id)

        if user is None:
            MessageQueue.push(session, Message('You must log into the application before you can view that page'))
            return redirect(reverse('login'))

        if user.tmp_password and password_change_redirect:
            MessageQueue.push(session, Message('You must change your password before accessing the application'))
            return redirect(reverse('users-edit', args=(user_id,)))

        user_type = UserAPI.check_user_type(user)

        if types is not None and len(types) > 0 and user_type not in types:

            if redirect_message is not None:
                MessageQueue.push(session, redirect_message)

            if redirect_to is None:
                redirect_to = redirect(reverse('index'))
            return redirect_to

        return user

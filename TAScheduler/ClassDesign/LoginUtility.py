import uuid
from typing import Union
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,reverse

from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.models import User


class LoginUtility:

    @staticmethod
    def update_password(user: User, password: str) -> str:
        user.password = password
        user.tmp_password = False
        user.save()

    @staticmethod
    def generate_tmp_password(self) -> str:
        return str(uuid.uuid4())[:8]

    @staticmethod
    def get_user_and_validate_by_user_id(
            session,
            types: list[UserType] = [],
            redirect_to : HttpResponseRedirect = redirect(reverse('index'))
    ) -> Union[User,HttpResponseRedirect]:
        """
        Get a user from a request context and validate the user's type
        To ensure that the user has permission to look at this page at this time
        """
        try:
            user_id = session['user_id']
        except KeyError:
            user_id = None

        if user_id is None or type(user_id) is not int:
            return redirect(reverse('login'))

        user = UserAPI.get_user_by_user_id(user_id)

        if user is None:
            return redirect(reverse('login'))

        if user.tmp_password:
            return redirect(reverse('user-edit', args=(user_id,)))

        user_type = UserAPI.check_user_type(user)

        if len(types)>0 and user_type not in types:
            return redirect_to

        return user
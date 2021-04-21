from TAScheduler.models import User
from typing import Union
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,reverse
from TAScheduler.ClassDesign.UserAPI import UserAPI


class LoginUtility:

    @staticmethod
    def update_password(user: User, password: str) -> str:
        user.password = password
        user.tmp_password = False
        user.save()

    @staticmethod
    def get_user_and_validate_by_user_id(user_id: int) -> Union[User,HttpResponseRedirect]:
        user = UserAPI.get_user_by_user_id(user_id)
        if user is None:
            return redirect(reverse('login'))
        if user.tmp_password:
            return redirect(reverse('user-edit', args=user_id))
        return user
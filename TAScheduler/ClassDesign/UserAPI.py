from TAScheduler.models import User, UserType
from typing import Union
from django.http import HttpResponseRedirect
from typing import Optional
from django.shortcuts import redirect,reverse


class UserAPI:

    @staticmethod
    ##should admin only enter this info or can admin add other info (lname, fname, phone) of user
    def create_user(type: UserType, univ_id: str, password: str, lname: str='', fname: str='',
                    phone: str='') -> int:
        new_user = User.objects.create(type=type, univ_id=univ_id, password=password, l_name=lname, f_name=fname, phone=phone)
        # new_user.save(),
        return new_user.user_id

    @staticmethod
    def get_user_by_user_id(user_id) -> Optional[User]:
        query_set = User.objects.filter(user_id = user_id)
        if len(query_set) > 0:
            return query_set[0]
        else:
            return None

    @staticmethod
    def get_user_by_univ_id(univ_id: str) -> Optional[User]:
        query_set = User.objects.filter(univ_id = univ_id)
        if len(query_set) > 0:
            return query_set[0]
        else:
            return None

    @staticmethod
    def delete_user(user: User, keep_parents=False):
        user.delete()

    @staticmethod
    def check_user_type(user: User):
        if user.type == UserType.ADMIN.value[0]:
            return UserType.ADMIN
        elif user.type == UserType.PROF.value[0]:
            return UserType.PROF
        else:
            return UserType.TA

    @staticmethod
    def update_user(user: User, lname: Optional[str] = None, fname: Optional[str] = None, phone: Optional[str] = None):
        # if attribute is none don't update database
        # for example, if lname passed is not none, the execute that
        user.l_name = lname
        user.f_name = fname
        user.phone = phone
        user.save()








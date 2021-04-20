from TAScheduler.models import User, UserType
from typing import Optional


class UserAPI:

    @staticmethod
    ##should admin only enter this info or can admin add other info (lname, fname, phone) of user
    def create_user(type: UserType, univ_id: str, password: str, lname: str='', fname: str='',
                    phone: str='') -> int:
        new_user = User(type=type, univ_id=univ_id, password=password, l_name=lname, f_name=fname, phone=phone)
        new_user.save(),
        return new_user.user_id


    @staticmethod
    def get_user_by_user_id(user_id) -> Optional[User]:
        query_set = User.objects.filter(user_id = user_id)
        if len(query_set) > 0:
            return query_set[0]
        else:
            return None

    @staticmethod
    def get_user_by_univ_id(univ_id) -> Optional[User]:
        query_set = User.objects.filter(univ_id = univ_id)
        if len(query_set) > 0:
            return query_set[0]
        else:
            return None

    @staticmethod
    def delete_user(user: User, keep_parents=False):
        user.delete()

    @staticmethod
    def update_user(user: User, lname: Optional[str], fname: str, phone: str):
        user.l_name = lname
        user.f_name = fname
        user.phone = phone
        user.save()



    @staticmethod
    def update_password(user: User, password: str):
        pass

    @staticmethod
    def change_password(self):
        pass

    @staticmethod
    def checck_user_type(user: User):
        pass















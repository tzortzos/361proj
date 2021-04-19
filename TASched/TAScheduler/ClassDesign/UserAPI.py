from TAScheduler.models import User, UserType


class UserAPI:

    @staticmethod
    ##should admin only enter this info or can admin add other info (lname, fname, phone) of user
    def create_user(type: UserType, univ_id: str, lname: str, fname: str, phone: str, password: str) -> int:
        new_user = User(type=type, univ_id=univ_id, l_name=lname, f_name=fname, phone=phone, password=password)
        new_user.save()
        return new_user.user_id


    @staticmethod
    def get_user_by_user_id(user_id) -> User:
        query_set = User.objects.filter(user_id = user_id)
        return query_set[0]


    @staticmethod
    def get_user_by_univ_id(univ_id) -> User:
        query_set = User.objects.filter(univ_id = univ_id)
        if len(query_set) > 0:
            return query_set[0]
        else:
            raise LookupError

    @staticmethod
    def delete_user(user: User, keep_parents=False):
        user.delete()

    @staticmethod
    def update_user(user: User, lname: str, fname: str, phone: str):
        user.lname = lname
        user.fname = fname
        user.phone = phone
        user.save()

    @staticmethod
    def update_password(user: User, password: str):
        pass













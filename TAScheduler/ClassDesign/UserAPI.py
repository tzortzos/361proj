from TAScheduler.models import User, UserType
from typing import Union, Iterable, Optional
from django.core.exceptions import ObjectDoesNotExist
import more_itertools


class UserAPI:

    @staticmethod
    def create_user(
            user_type: Union[UserType, str],
            univ_id: str,
            password: str,
            lname: str = '',
            fname: str = '',
            phone: str = ''
    ) -> int:
        """
        Create User with mandatory user type, univ_id(front end email), and password, returns user id
        """
        if type(user_type) is str:
            user_type = UserType.from_str(user_type)

        if univ_id is None or univ_id == '':
            raise TypeError('username cannot be blank')

        if password is None or password == '':
            raise TypeError('password cannot be blank')

        new_user = User.objects.create(
            type=user_type,
            username=univ_id,
            password=password,
            l_name=lname,
            f_name=fname,
            phone=phone
        )
        return new_user.id

    @staticmethod
    def get_user_by_user_id(user_id) -> Optional[User]:
        """
        Get user by user id and returns User if it exists, otherwise returns None
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_univ_id(univ_id: str) -> Optional[User]:
        """
        Get user by university id and returns User if it exists, otherwise returns None
        """
        try:
            return User.objects.get(username=univ_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_all_users() -> Optional[Iterable[User]]:
        """
        Get all users if any exist otherwise return None
        """
        user_set = User.objects.all()
        return user_set if more_itertools.ilen(user_set) > 0 else None
        # try:
        #     return User.objects.all()
        # except User.DoesNotExist:
        #     return None

    @staticmethod
    def delete_user(id: int, keep_parents=False) -> bool:
        """
        Deletes User if it exists using the id and returns a boolean for confirmation
        """
        try:
            user = User.objects.get(id=id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            return False

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
        """
        Updates user for last name, first name, and phone.
        If field is None then does not update, if empty string then removes current.
        """
        if lname is not None:
            user.l_name = lname

        if fname is not None:
            user.f_name = fname

        if phone is not None:
            user.phone = phone

        user.save()

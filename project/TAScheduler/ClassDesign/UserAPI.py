from project.TAScheduler.models import User, UserType


class UserAPI():

    @staticmethod
    def create_user(type: UserType, univ_id: str, password: str)-> int:
        new_user = User(type=type, univ_id=univ_id,password=password)
        new_user.save()
        return new_user.user_id


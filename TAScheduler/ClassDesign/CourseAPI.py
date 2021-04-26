from TAScheduler.models import Course, User, UserType
from typing import Optional, Union, Type, Iterable



class CourseAPI:

    @staticmethod
    def create_course(code: str, name: str, admin: User) -> Union[int, Type[TypeError]]:
        if code is '' or name is '':
            raise TypeError('code or name is empty.')
        new_course = Course.objects.create(course_code=code, course_name=name, admin_id=admin)
        return new_course.course_id

    @staticmethod
    def get_course_by_course_code(code: str) -> Optional[Course]:
        try:
            course = Course.objects.get(course_code=code)
            return course
        except Course.DoesNotExist:
            return None

    @staticmethod
    def get_course_by_course_id(id: int) -> Optional[Course]:
        try:
            course = Course.objects.get(course_id=id)
            return course
        except Course.DoesNotExist:
            return None

    @staticmethod
    def get_all_courses() -> Iterable[Course]:
        return Course.objects.all()

    @staticmethod
    def delete_course(course: Course) -> None:
        course.delete()

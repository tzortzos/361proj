from TAScheduler.models import Course, User, UserType
from typing import Optional


class CourseAPI:

    @staticmethod
    def create_course(code: str, name: str, admin: User):
        # this create is different than save() in that it creates and saves simultaneously
        # do we want the course_id (autogenerated) returned or course object?
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
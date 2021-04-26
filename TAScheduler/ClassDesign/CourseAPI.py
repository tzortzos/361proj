from TAScheduler.models import Course, User, UserType
from typing import Optional, Union, Type, Iterable
import more_itertools


class CourseAPI:

    @staticmethod
    def create_course(code: str, name: str, admin: User) -> Union[int, TypeError]:
        """
        Creates a course by taking a code and name with admin log, raises TypeError if argument issue
        """
        if code is '' or name is '':
            raise TypeError('Course code or Course name can\'t be empty.')
        new_course = Course.objects.create(course_code=code, course_name=name, admin_id=admin)
        return new_course.course_id

    @staticmethod
    def get_course_by_course_code(code: str) -> Optional[Course]:
        """
        Gets a course by its course_code, if it exists or returns None
        """
        try:
            course = Course.objects.get(course_code=code)
            return course
        except Course.DoesNotExist:
            return None

    @staticmethod
    def get_course_by_course_id(id: int) -> Optional[Course]:
        """
        Gets a course by its course_id, if it exists
        """
        try:
            course = Course.objects.get(course_id=id)
            return course
        except Course.DoesNotExist:
            return None

    @staticmethod
    def get_all_courses() -> Optional[Iterable[Course]]:
        """
        Gets all courses from the database, if they exist
        """
        set = Course.objects.all()
        return set if more_itertools.ilen(set) > 0 else None

    @staticmethod
    def edit_course(id: int) -> bool:
        pass


    @staticmethod
    def delete_course(id: int) -> bool:
        """
        Deletes course, if it exists, using a course_id value, returns boolean to confirm
        """
        global course
        try:
            course = Course.objects.get(course_id=id)
            course.delete()
            return True
        except course.DoesNotExist:
            return False



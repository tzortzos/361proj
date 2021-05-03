from TAScheduler.models import Course, User, UserType, Section
from typing import Optional, Iterable
from django.core.exceptions import ObjectDoesNotExist


class SectionAPI:

    @staticmethod
    def create_course_section(
            code: str,
            course: Course,
            days: str = '',
            time: str = '',
            prof: User = None,
    ) -> int:
        """
        Creates new course section associated to Course, returns the course section id primary key.
        """
        if code == '' or course == None:
            raise TypeError("Code or Course cannot be blank.")
        new_course_section = Section.objects.create(
            code=code,
            course=course,
            days=days,
            time=time,
            prof=prof)

        return new_course_section.id

    @staticmethod
    def get_by_id(id: int) -> Optional[Section]:
        """
        Get course section by id if it exists, returns the course section object or none
        """
        try:
            return Section.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_for_course(course_id: Course) -> Optional[Iterable[Section]]:
        """
        Get all course sections associated with a course if any exist otherwise returns none
        """
        try:
            return Section.objects.filter(course=course_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_by_id(id: int) -> bool:
        """
        Deletes course section if it exists, returns boolean for confirmation
        """
        try:
            section = Section.objects.get(id=id)
            section.delete()
            return True
        except ObjectDoesNotExist:
            return None



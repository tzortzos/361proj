from TAScheduler.models import Course, User, UserType, Section
from typing import Optional, Iterable
from django.core.exceptions import ObjectDoesNotExist


class SectionAPI:

    @staticmethod
    def create_course_section(
            section_code: str,
            course_id: Course,
            days: str = '',
            time: str = '',
            professor: User = None,
    ) -> int:
        """
        Creates new course section associated to Course, returns the course section id primary key.
        """
        new_course_section = Section(
            code=section_code,
            course=course_id,
            days=days,
            time=time,
            prof=professor)
        new_course_section.save()

        return new_course_section.id

    @staticmethod
    def get_by_id(id: str) -> Optional[Section]:
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
            return False



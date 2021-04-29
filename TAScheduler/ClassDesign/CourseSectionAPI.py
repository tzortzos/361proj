from TAScheduler.models import Course, User, UserType, Section
from typing import Optional, Iterable
from django.core.exceptions import ObjectDoesNotExist


class CourseSectionAPI:

    @staticmethod
    def create_course_section(
            section_code: str,
            course_id: Course,
            days: str = '',
            time: str = '',
            instructor: User = None,
    ) -> int:
        """
        Creates new course section associated to Course, returns the course section id primary key.
        """
        new_course_section = Section(
            course_section_code=section_code,
            course_id=course_id,
            lecture_days=days,
            lecture_time=time,
            instructor_id=instructor)
        new_course_section.save()

        return new_course_section.id

    @staticmethod
    def get_course_section_by_course_id(id: str) -> Optional[Section]:
        """
        Get course section by id if it exists, returns the course section object or none
        """
        try:
            return Section.objects.get(course_section_id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_course_sections_for_course(course_id: Course) -> Optional[Iterable[Section]]:
        """
        Get all course sections associated with a course if any exist otherwise returns none
        """
        try:
            return Section.objects.filter(course_id=course_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def delete_course_section(id: int)-> bool:
        """
        Deletes course section if it exists, returns boolean for confirmation
        """
        try:
            section = Section.objects.get(course_section_id=id)
            section.delete()
            return True
        except ObjectDoesNotExist:
            return False



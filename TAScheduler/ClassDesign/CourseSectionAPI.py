from TAScheduler.models import Course, User, UserType, CourseSection
from typing import Optional, List


class CourseSectionAPI:

    @staticmethod
    def create_course_section(section_code: str, course_id: Course, days: str = '', time: str = '',
                              instructor: User = None) -> int:
        new_course_section = CourseSection(course_section_code=section_code, course_id=course_id, lecture_days=days,
                                           lecture_time=time, instructor_id=instructor)
        new_course_section.save()
        return new_course_section.course_section_id

    #Should the get method be simply
    @staticmethod
    def get_course_section_by_course_id(course_section_code: str, course_id: Course) -> CourseSection:
        return CourseSection.objects.get(course_section_code=course_section_code, course_id=course_id)

    @staticmethod
    def get_all_course_sections_for_course(course_id: Course) -> List[CourseSection]:
        return CourseSection.objects.filter(course_id=course_id)

    @staticmethod
    def delete_course_section(course_section: int):
        pass

    @staticmethod
    def delete_course_section(course_section: CourseSection) -> None:
        course_section.delete()
        print("Deleted course section" + str(course_section))



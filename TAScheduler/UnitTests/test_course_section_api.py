from TAScheduler.ClassDesign.CourseSectionAPI import CourseSectionAPI
from TAScheduler.models import UserType,User,Course, CourseSection
from django.test import TestCase


class TestCourseSection(TestCase):

    def setUp(self) -> None:
        self.course_section_code1 = '901'
        self.lecture_days1 = 'MWF'
        self.lecture_time1 = '12-2p'
        course = Course.objects.create(course_code='361', course_name='TestCourse')
        self.course_id1 = course

    def test_create_course_section(self):
        new_course_section_id = CourseSectionAPI.create_course_section(self.course_section_code1, self.course_id1,
                                                                       self.lecture_days1, self.lecture_time1, None)
        self.assertTrue(new_course_section_id > 0, msg='Expecting new id returned confirming saved to database.')

    def test_get_course_section_by_course_id(self):
        course_section1 = CourseSection.objects.create(course_section_code=self.course_section_code1,
                                                       course_id=self.course_id1)
        course_section2 = CourseSectionAPI.get_course_section_by_course_id(course_id: Course)
        pass


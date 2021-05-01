import uuid
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from TAScheduler.ClassDesign.CourseSectionAPI import CourseSectionAPI
from TAScheduler.ClassDesign.CourseAPI import CourseAPI
from TAScheduler.models import Course, CourseSection


class TestCourseSection(TestCase):

    def setUp(self) -> None:

        self.course_section_code1 = str(uuid.uuid4())[:3]
        self.course_section_code2 = str(uuid.uuid4())[:3]
        self.lecture_days1 = 'MWF'
        self.lecture_days2 = 'TTh'
        self.lecture_time1 = '12-2p'
        self.lecture_time2 = '3-5p'

        self.course_code = str(uuid.uuid4())[:3]
        self.course_code2 = str(uuid.uuid4())[:3]
        self.course_id1 = Course.objects.create(course_code=self.course_code, course_name='TestCourse')
        self.course_id2 = Course.objects.create(course_code=self.course_code2, course_name='TestCourse2')

        self.course_section1 = CourseSection.objects.create(
            course_section_code=self.course_section_code1,
            course_id=self.course_id1)

        self.course_section2 = CourseSection.objects.create(
            course_section_code=self.course_section_code2,
            course_id=self.course_id1
        )

    def test_create_course_section(self):
        new_course_section_id = CourseSectionAPI.create_course_section('903', self.course_id1)
        self.assertTrue(new_course_section_id > 0, msg='Expecting new id returned confirming saved to database.')

    def test_get_course_section_by_course_id(self):
        course_section3 = CourseSectionAPI.get_course_section_by_course_id(self.course_section1.course_section_id)
        self.assertEqual(self.course_section1, course_section3, msg='Expected course1 to be course2 after call to get.')

    def test_get_all_course_sections_for_course(self):
        query_set = CourseSectionAPI.get_all_course_sections_for_course(self.course_id1)
        self.assertTrue(self.course_section1 in query_set, msg='Expected course_section1 in list of course sections.')
        self.assertTrue(self.course_section2 in query_set, msg='Expected course_section2 in list of course sections.')

    def test_delete_course_section(self):
        CourseSectionAPI.delete_course_section(self.course_section2.course_section_id)
        with self.assertRaises(ObjectDoesNotExist, msg="Expected the course section to be deleted"):
            CourseSection.objects.get(course_section_id=self.course_section2.course_section_id)

    def test_get_course_section_by_course_id_not_in_database(self):
        response = CourseSectionAPI.get_course_section_by_course_id(self.course_code2)
        self.assertEqual(None, response, msg="Expected None when course does not exist in database.")

    def test_rejects_empty_course_section_code(self):
        with self.assertRaises(TypeError, msg='Course section code should not be blank.'):
            CourseSectionAPI.create_course_section('', self.course_id1, self.user1)

    def test_rejects_empty_course_section_id(self):
        with self.assertRaises(TypeError, msg='Course section id should not be blank.'):
            CourseSectionAPI.create_course_section(self.course_code, None)

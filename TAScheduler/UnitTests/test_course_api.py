from TAScheduler.ClassDesign.CourseAPI import CourseAPI
from TAScheduler.models import UserType,User,Course
from django.test import TestCase


class TestCourse(TestCase):

    def setUp(self):
        self.course_code1 = '123'
        self.course_code2 = '456'
        self.course_name1 = 'TestCourse'
        self.user1 = User.objects.create(type=UserType.ADMIN, univ_id='bsmith', password='password123')
        self.course1 = Course.objects.create(course_code=self.course_code1,course_name=self.course_name1,admin_id=self.user1)

    def test_create_course(self):
        new_course_id = CourseAPI.create_course(self.course_code1, self.course_name1, self.user1)
        self.assertTrue(new_course_id > 0, msg='Expecting the course Id to be a positive integer if added.')

    def test_get_course_by_course_code(self):
        course2 = CourseAPI.get_course_by_course_code(self.course_code1)
        self.assertEqual(self.course1, course2, msg="Expected the course to be retrieved by its course code.")

    def test_get_course_by_course_code_not_in_database(self):
        response = CourseAPI.get_course_by_course_code(self.course_code2)
        self.assertEqual(None, response, msg="Expected None when course does not exist in database.")

    def test_get_course_by_course_id(self):
        course_id = self.course1.course_id
        course = CourseAPI.get_course_by_course_id(course_id)
        self.assertEqual(course, self.course1, msg="Expected course1 when using its course id to retrieve.")

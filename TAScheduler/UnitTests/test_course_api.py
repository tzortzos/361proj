from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
import uuid
import more_itertools

from TAScheduler.ClassDesign.CourseAPI import CourseAPI
from TAScheduler.models import UserType,User,Course


class TestCourse(TestCase):

    def setUp(self):
        self.course_code1 = '360'
        self.course_code2 = str(uuid.uuid4())[:3]
        self.course_code3 = str(uuid.uuid4())[:3]
        self.course_name1 = 'TestCourse'
        self.course_name2 = 'TestCourse2'
        self.user1 = User.objects.create(type=UserType.ADMIN, username='bsmith', password='password123')
        self.course1 = Course.objects.create(code=self.course_code1,name=self.course_name1)
        self.course2 = Course.objects.create(code=self.course_code2,name=self.course_name2)

    def test_create_course(self):
        new_course_id = CourseAPI.create_course(self.course_code1, self.course_name1)
        self.assertTrue(new_course_id > 0, msg='Expecting the course Id to be a positive integer if added.')

    def test_rejects_empty_course_code(self):
        with self.assertRaises(TypeError, msg='Course code should not be blank.'):
            CourseAPI.create_course('', self.course_name1)

    def test_rejects_empty_course_name(self):
        with self.assertRaises(TypeError, msg='Course name should not be blank.'):
            CourseAPI.create_course(self.course_code1, '')

    def test_get_course_by_course_code(self):
        course2 = CourseAPI.get_course_by_course_code(self.course_code1)
        self.assertEqual(self.course1, course2, msg="Expected the course to be retrieved by its course code.")

    def test_get_course_by_course_code_not_in_database(self):
        response = CourseAPI.get_course_by_course_code(self.course_code3)
        self.assertEqual(None, response, msg="Expected None when course does not exist in database.")

    def test_get_course_by_course_id(self):
        course = CourseAPI.get_course_by_course_id(self.course1.id)
        self.assertEqual(course, self.course1, msg="Expected course1 when using its course id to retrieve.")

    def test_get_all_courses(self):
        course_set = CourseAPI.get_all_courses()
        list_of_courses = list(course_set)
        length = more_itertools.ilen(list_of_courses)
        self.assertEqual(2, length, msg='Expected list of courses to be 2.')
        self.assertTrue(self.course1 in list_of_courses, msg='Exepect course1 in all courses.')
        self.assertTrue(self.course2 in list_of_courses, msg='Expected course2 in all courses.')

    def test_delete_course(self):
        response = CourseAPI.delete_course(self.course1.id)
        self.assertEqual(True, response, msg='Expected a course that exists and was deleted to return true.')

    def test_delete_course_not_in_db(self):
        response1 = CourseAPI.delete_course(self.course2.id)
        response2 = CourseAPI.delete_course(self.course2.id)
        self.assertEqual(False, response2, msg='Expected a delete call on a course that didn\'t exist tor return true.')
        # with self.assertRaises(ObjectDoesNotExist, msg="Expected the Course to be deleted from database."):
        #     Course.objects.get(course_code=self.course1.course_code)


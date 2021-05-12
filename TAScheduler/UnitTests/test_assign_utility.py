import uuid
from TAScheduler.ClassDesign.AssignUtility import AssignUtility
from TAScheduler.models import User, UserType,Section, Course,Assignment, Lab

from django.test import TestCase


class TestAssignUtility(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(type=UserType.TA, username='bsmith', password='Password123')
        self.user2 = User.objects.create(type=UserType.TA, username='sfarley', password='Password456')
        self.user3 = User.objects.create(type=UserType.PROF, username='iamprof',password='Password789')
        self.course1 = Course.objects.create(code='361',name='SoftwareEngineering')
        self.code1 = str(uuid.uuid4())[:3]
        self.code2 = str(uuid.uuid4())[:3]
        self.section1 = Section.objects.create(code=self.code1, course=self.course1)
        self.section2 = Section.objects.create(code=self.code2, course=self.course1)
        self.user4 = User.objects.create(type=UserType.PROF, username='iamprof2', password='Password')
        self.section2.prof = self.user4
        self.assignment1 = Assignment.objects.create(ta=self.user1,section=self.section1, max_labs=1)
        self.assignment2 = Assignment.objects.create(ta=self.user3,section=self.section1, max_labs=2)
        self.code3 = str(uuid.uuid4())[:3]
        self.code4 = str(uuid.uuid4())[:3]
        self.Lab1 = Lab.objects.create(code=self.code3, section=self.section1, ta=self.user1)
        self.Lab2 = Lab.objects.create(code=self.code4, section=self.section1, ta=self.user2)
        self.Lab3 = Lab.objects.create(code=str(uuid.uuid4())[:3], section=self.section1)

    def test_assign_prof_to_section(self):
        self.assertTrue(AssignUtility.assign_prof_to_section(self.user3,self.section1))

    def test_section_already_has_prof_assign(self):
        self.assertFalse(AssignUtility.assign_prof_to_section(self.user4, self.section2))

    def test_remove_prof_from_section(self):
        self.assertTrue(AssignUtility.remove_prof_from_section(self.user4, self.section2))

    def test_assign_ta_to_section(self):
        response = AssignUtility.assign_ta_to_section(self.user2, self.section1, 2)
        self.assertEqual(True, response, msg='Expected the TA to be added to section.')

    def test_ta_already_assigned_to_section(self):
        response = AssignUtility.assign_ta_to_section(self.user1, self.section1, 1)
        self.assertEqual(False, response, msg="Expected the TA not to be added because already assigned.")

    def test_remove_ta_from_section(self):
        self.assertTrue(AssignUtility.remove_ta_from_section(self.user1, self.section1))
        qs = self.section1.tas.all()
        self.assertTrue(self.user1 not in qs, msg='Expected user1 to be removed from list of tas')

    def test_check_ta_assign_number(self):
        self.assertFalse(AssignUtility.check_ta_assign_number(self.user1, self.section1))

    def tests_check_ta_assign_number_good(self):
        self.assertTrue(AssignUtility.check_ta_assign_number(self.user3, self.section1))

    def test_update_ta_assign_number(self):
        self.assertTrue(AssignUtility.update_ta_assign_number(self.user3, self.section1, 4))
        self.assignment2.refresh_from_db()
        self.assertEqual(4, self.assignment2.max_labs, msg='Expected new max_lab value to be 4.')

    def test_assign_ta_to_lab(self):
        user = User.objects.create(type=UserType.TA, username='newuser', password='PasswordMe')
        self.assertTrue(AssignUtility.assign_ta_to_lab(user,self.Lab3))
        self.Lab3.ta.refresh_from_db()
        self.assertEqual(user, self.Lab3.ta, msg='Expected user3 to be the TA assigned to Lab3')

    def test_remove_ta_from_lab(self):
        self.assertTrue(AssignUtility.remove_ta_from_lab(self.user1, self.Lab1))
        self.assertEqual(None, self.Lab1.ta, msg='Expected Lab1 TA to be none after removal.')


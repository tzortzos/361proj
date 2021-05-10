import uuid
from TAScheduler.ClassDesign.AssignUtility import AssignUtility
from TAScheduler.models import User, UserType,Section, Course,Assignment

from django.test import TestCase


class TestAssignUtility(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(type=UserType.TA, username='bsmith', password='Password123')
        self.user2 = User.objects.create(type=UserType.TA, username='sfarley', password='Password456')
        self.course1 = Course.objects.create(code='361',name='SoftwareEngineering')
        self.code = str(uuid.uuid4())[:3]
        self.section1 = Section.objects.create(code=self.code, course=self.course1)
        self.assignment1 = Assignment.objects.create(ta=self.user1,section=self.section1, max_labs=1)

    def test_assign_ta_to_section(self):
        response = AssignUtility.assign_ta_to_section(self.user2, self.section1, 2)
        self.assertEqual(True, response, msg='Expected the TA to be added to section.')

    def test_ta_already_assigned_to_section(self):
        response = AssignUtility.assign_ta_to_section(self.user1, self.section1, 1)
        self.assertEqual(False, response, msg="Expected the TA not to be added because already assigned.")

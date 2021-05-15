
from django.test import TestCase
from TAScheduler.ClassDesign.SkillsUtility import SkillsUtility
from TAScheduler.models import Skill, Course, UserType, User


class TestSkillsUtility(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(type=UserType.TA, username='bsmith', password='Mandatory')
        self.skill1 = Skill.objects.create(name='Python')
        self.skill2 = Skill.objects.create(name='Database')
        self.course1 = Course.objects.create(code='361', name='Software Engineering')

    def test_length_skill(self):
        self.assertFalse(SkillsUtility.create_skill('hddhjdkdldldhdlfhdifdhdhfdhfhdfkhdf'))

    def test_create_skill(self):
        self.assertTrue(SkillsUtility.create_skill('Django'))

    def test_skill_already_in_list(self):

        self.assertTrue(SkillsUtility.create_skill(self.skill1.name))

    def test_add_skill_to_course(self):
        self.assertTrue(SkillsUtility.add_skill_to_course(self.skill1.id ,self.course1.id))

    def test_remove_skill_from_course(self):
        self.course1.preferred_skills.add(self.skill1)
        self.assertTrue(SkillsUtility.remove_skill_from_course(self.skill1.id, self.course1.id))

    def test_add_skill_to_ta(self):
        self.assertTrue(SkillsUtility.add_skill_to_ta(self.user1.id, [self.skill1.id, self.skill2.id]))
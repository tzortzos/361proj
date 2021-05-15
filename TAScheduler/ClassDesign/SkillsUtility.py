from typing import List
from TAScheduler.models import User, Skill, Course, UserType
from django.db.utils import IntegrityError


class SkillsUtility:

    @staticmethod
    def create_skill(skill_name: str) -> bool:
        """
        Creates a new skill in the global list of skills that are avaialble to be assigned to course
        or linked to TA
        """
        if len(skill_name) > 30: return False
        try:
            Skill.objects.create(name=skill_name)
        except IntegrityError:
            pass
        return True


    @staticmethod
    def add_skill_to_course(skill_id: int, course_id: int) -> bool:
        """
        Adds a desired skill to have have for TAs to have when TAing this course
        """
        course = Course.objects.get(id=course_id)
        skill = Skill.objects.get(id=skill_id)
        if skill not in course.preferred_skills.all():
            course.preferred_skills.add(skill)
            return True
        else:
            return False

    @staticmethod
    def remove_skill_from_course(skill_id: int, course_id: int) -> bool:
        # preferred skills in course
        course = Course.objects.get(id=course_id)
        skill = Skill.objects.get(id=skill_id)
        if skill in course.preferred_skills.all():
            skill.delete()
            return True
        return False

    @staticmethod
    def add_skill_to_ta(user_id: int, skills: List[int]) -> bool:

        # User.skills
        user = User.objects.get(id=user_id)
        if user.type == UserType.TA:
            for item_id in skills:
                skill = Skill.objects.get(id=item_id)
                user.skills.add(skill)
            return True
        else:
            return False


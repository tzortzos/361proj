import uuid

from TAScheduler.ClassDesign.LabSectionAPI import LabSectionAPI
from TAScheduler.models import UserType, CourseSection, Course, User
from django.test import TestCase


class TestLabSection(TestCase):

    def setUp(self) -> None:
        self.lab_section_code = str(uuid.uuid4())[:3]
        self.course_section_id = CourseSection.objects.create(
            course_section_code=str(uuid.uuid4())[:3],
            course_id= Course.objects.create(
                course_code=str(uuid.uuid4())[:3],
                course_name='Software Engineering',
                admin_id=User.objects.create(
                    type=UserType.ADMIN,
                    univ_id='bsmith',
                    password='password123')
            )
        )

    def test_create_lab_section(self):
        lab_id = LabSectionAPI.create_lab_section(self.lab_section_code, self.course_section_id)
        self.assertTrue(lab_id > 0, msg='Expected a lab_id key returned indicating created and saved in database.')




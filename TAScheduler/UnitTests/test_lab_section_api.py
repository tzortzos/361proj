import uuid
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from TAScheduler.ClassDesign.LabSectionAPI import LabSectionAPI
from TAScheduler.models import UserType, CourseSection, Course, User, LabSection


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
        self.labsection1 = LabSection.objects.create(
            lab_section_code=str(uuid.uuid4())[:3],
            course_section_id=self.course_section_id)

        self.labsection2 = LabSection.objects.create(
            lab_section_code=str(uuid.uuid4())[:3],
            course_section_id=self.course_section_id)

    def test_create_lab_section(self):
        lab_id = LabSectionAPI.create_lab_section(self.lab_section_code, self.course_section_id)
        self.assertTrue(lab_id > 0, msg='Expected a lab_id key returned indicating created and saved in database.')

    def test_get_lab_section_by_lab_id(self):
        new_lab = LabSection.objects.create(
            lab_section_code=self.lab_section_code,
            course_section_id=self.course_section_id)
        lab = LabSectionAPI.get_lab_section_by_lab_id(new_lab.lab_section_id)
        self.assertEqual(new_lab, lab, msg='Expected to get a lab section object returned by new lab id.')

    def test_get_all_lab_sections_from_course_section_and_course(self):
        list_of_labs = LabSectionAPI.get_all_lab_sections_from_course_section_and_course(
            self.course_section_id
        )
        self.assertTrue(self.labsection1 in list_of_labs, msg='Expected labs section 1 in the list for course section.')
        self.assertTrue(self.labsection2 in list_of_labs, msg='Expected labs section 1 in the list for course section.')

    def test_edit_lab_section(self):
        new_lab = LabSection.objects.create(
            lab_section_code=str(uuid.uuid4())[:3],
            course_section_id=self.course_section_id)

        ta = User.objects.create(
            type=UserType.TA,
            univ_id='alarry',
            password='Password123',
        )
        self.lab_days = 'MWF'

        LabSectionAPI.edit_lab_section(
            new_lab.lab_section_id,
            lab_days=self.lab_days,
            lab_time='1-3p',
            ta_id=ta
        )

        new_lab = LabSection.objects.get(lab_section_id=new_lab.lab_section_id)

        self.assertEquals(self.lab_days, new_lab.lab_days, msg='Expected update of lab days to MWF.')
        self.assertEqual('1-3p', new_lab.lab_time, msg='Expected update of lab time to 1-3p.')
        self.assertEqual(ta, new_lab.ta_id, msg='Expected update of assigned ta to ta.')

    def test_delete_lab_section(self):
        LabSectionAPI.delete_lab_section(self.labsection1.lab_section_id)
        with self.assertRaises(ObjectDoesNotExist, msg="Expected the lab section to be deleted."):
            LabSection.objects.get(lab_section_id=self.labsection1.lab_section_id)









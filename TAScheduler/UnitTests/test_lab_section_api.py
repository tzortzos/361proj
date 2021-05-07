import uuid
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from TAScheduler.ClassDesign.LabAPI import LabAPI
from TAScheduler.models import UserType, Section, Course, User, Lab


class TestLabSection(TestCase):

    def setUp(self) -> None:
        self.lab_section_code2 = ''
        self.lab_section_code = str(uuid.uuid4())[:3]
        self.lab_section_code2 = ''
        self.course_section_id = Section.objects.create(
            code=str(uuid.uuid4())[:3],
            course=Course.objects.create(
                code=str(uuid.uuid4())[:3],
                name='Software Engineering',
            )
        )
        self.labsection1 = Lab.objects.create(
            code=str(uuid.uuid4())[:3],
            section=self.course_section_id)

        self.labsection2 = Lab.objects.create(
            code=str(uuid.uuid4())[:3],
            section=self.course_section_id)

    def test_create_lab_section(self):
        lab_id = LabAPI.create_lab_section(self.lab_section_code, self.course_section_id)
        self.assertTrue(lab_id > 0, msg='Expected a lab_id key returned indicating created and saved in database.')

    def test_get_lab_section_by_lab_id(self):
        new_lab = Lab.objects.create(
            code=self.lab_section_code,
            section=self.course_section_id)
        lab = LabAPI.get_lab_section_by_lab_id(new_lab.id)
        self.assertEqual(new_lab, lab, msg='Expected to get a lab section object returned by new lab id.')

    def test_get_all_lab_sections_from_course_section_and_course(self):
        list_of_labs = LabAPI.get_all_lab_sections_for_course_section(
            self.course_section_id
        )
        self.assertTrue(self.labsection1 in list_of_labs, msg='Expected labs section 1 in the list for course section.')
        self.assertTrue(self.labsection2 in list_of_labs, msg='Expected labs section 1 in the list for course section.')

    def test_edit_lab_section(self):
        new_lab = Lab.objects.create(
            code=str(uuid.uuid4())[:3],
            section=self.course_section_id)

        ta = User.objects.create(
            type=UserType.TA,
            username='alarry',
            password='Password123',
        )
        self.lab_days = 'MWF'

        LabAPI.edit_lab_section(
            new_lab.id,
            day=self.lab_days,
            time='1-3p',
            ta=ta
        )

        new_lab = Lab.objects.get(id=new_lab.id)

        self.assertEquals(self.lab_days, new_lab.day, msg='Expected update of lab days to MWF.')
        self.assertEqual('1-3p', new_lab.time, msg='Expected update of lab time to 1-3p.')
        self.assertEqual(ta, new_lab.ta, msg='Expected update of assigned ta to ta.')

    def test_delete_lab_section(self):
        LabAPI.delete_lab_section(self.labsection1.id)
        with self.assertRaises(ObjectDoesNotExist, msg="Expected the lab section to be deleted."):
            Lab.objects.get(id=self.labsection1.id)

    def test_empty_section_code(self):
        with self.assertRaises(TypeError):
            LabAPI.create_lab_section(
                '',
                self.course_section_id,
            )






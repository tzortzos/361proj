import uuid
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from TAScheduler.ClassDesign.LabAPI import LabAPI
from TAScheduler.models import UserType, Section, Course, User, Lab


class TestLabSection(TestCase):

    def setUp(self) -> None:
        self.lab_code1 = str(uuid.uuid4())[:3]
        self.lab_code2 = str(uuid.uuid4())[:3]

        self.course_section_id = Section.objects.create(
            code=str(uuid.uuid4())[:3],
            course=Course.objects.create(
                code=str(uuid.uuid4())[:3],
                name='Software Engineering')
            )

        self.labsection1 = Lab.objects.create(
            code=self.lab_code1,
            section=self.course_section_id)

        self.labsection2 = Lab(
            code=self.lab_code2,
            section=self.course_section_id)

        self.labsection3 = Lab.objects.create(
            code=str(uuid.uuid4())[:3],
            section=self.course_section_id
        )

    def test_create_lab_section(self):
        lab_id = LabSectionAPI.create_lab_section(self.lab_code2, self.course_section_id)
        self.assertTrue(lab_id > 0, msg='Expected a lab_id key returned indicating created and saved in database.')

    def test_get_lab_section_by_lab_id(self):
        lab = LabSectionAPI.get_lab_section_by_lab_id(self.labsection1.id)
        self.assertEqual(self.labsection1, lab, msg='Expected to get a lab section object returned by lab id.')

    def test_get_lab_section_not_in_db(self):
        lab = LabSectionAPI.get_lab_section_by_lab_id(self.labsection2.id)
        self.assertEqual(None, lab, msg="Expected None because lab section does not exist in database.")

    def test_get_all_lab_sections_for_course_section(self):
        list_of_labs = LabSectionAPI.get_all_lab_sections_for_course_section(
            self.course_section_id
        )
        self.assertTrue(self.labsection1 in list_of_labs, msg='Expected labs section 1 in the list for course section.')
        self.assertTrue(self.labsection3 in list_of_labs, msg='Expected labs section 3 in the list for course section.')

    def test_edit_lab_section(self):

        ta = User.objects.create(
            type=UserType.TA,
            username='alarry',
            password='Password123',
        )
        self.lab_days = 'MWF'

        LabSectionAPI.edit_lab_section(
            self.labsection3.id,
            self.lab_days,
            '1-3p',
            ta
        )
        lab3 = Lab.objects.get(id=self.labsection3.id)

        self.assertEquals(self.lab_days, lab3.day, msg='Expected update of lab days to MWF.')
        self.assertEqual('1-3p', lab3.time, msg='Expected update of lab time to 1-3p.')
        self.assertEqual(ta, lab3.ta, msg='Expected update of assigned ta to ta.')

    def test_delete_lab_section(self):
        response = LabSectionAPI.delete_lab_section(self.labsection1.id)
        self.assertEqual(True, response, msg='Expected a return  of True for the delete.')

    def test_rejects_edit_empty_lab_section(self):
        with self.assertRaises(TypeError, msg='lab section should not be blank.'):
            LabAPI.edit_by_id(None)

    def test_empty_section_id(self):
        new_lab = Lab.objects.create(
            code=self.lab_section_code2,
            section=self.course_section_id)
        lab = LabSectionAPI.get_lab_section_by_lab_id(new_lab.id)
        self.assertTrue(lab.code, msg='Lab section ID can not be blank!')






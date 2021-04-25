from typing import Optional, Union

from TAScheduler.models import User, CourseSection
from TAScheduler.models import LabSection


class LabSectionAPI:

    @staticmethod
    def create_lab_section(
            lab_section_code: str,
            course_section_id: CourseSection,
            lab_days: str = '',
            lab_time: str = '',
            ta_id: User = None,
    ) -> int:
        """
        Create Lab section with a lab_section code and the Course Section to which it is associated.
        lab_section_id is autogenerated
        """
        new_lab_section = LabSection.objects.create(
            lab_section_code=lab_section_code,
            course_section_id=course_section_id,
            lab_days=lab_days,
            lab_time=lab_time,
            ta_id=ta_id
        )
        return new_lab_section.lab_section_id

    @staticmethod
    def get_lab_section_by_lab_id(lab: int) -> Optional[LabSection]:
        """
        Using the autogenerated primary key lab_section_id; returns a LabSection object, if it exists
        """
        return LabSection.objects.get(lab_section_id=lab)

    @staticmethod
    def get_all_lab_sections_from_course_section_and_course(course_section_id: int) -> list[LabSection]:
        """
        Returns all LabSection objects associated with a specific course section id, if any exist
        """
        return LabSection.objects.filter(course_section_id=course_section_id)


    @staticmethod
    def edit_lab_section(
            lab_section: int,
            lab_days: Optional[str]= None,
            lab_time: Optional[str]=None,
            ta_id: Optional[User]=None
    ) -> None:
        """
        Using the lab_secton_id primary key of the lab, updates lab_days, lab_time, and ta_id, if it exists
        """
        lab = LabSection.objects.get(lab_section_id=lab_section)
        lab.lab_days = lab_days
        lab.lab_time = lab_time
        lab.ta_id = ta_id
        lab.save()


    @staticmethod
    def delete_lab_section(
          lab_section: int
    ) -> None:
        """
        Using the lab_section id primary key, deletes user if it exists.
        """
        LabSection.objects.get(lab_section_id=lab_section).delete()

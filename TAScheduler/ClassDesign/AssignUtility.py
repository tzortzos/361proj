from TAScheduler.models import User, Section, Lab, Assignment, UserType
from typing import List, Tuple


class AssignUtility:

    @staticmethod
    def assign_prof_to_section(user: User, section: Section) -> bool:
        """
        Assigns a Prof to a Section if there has not been one already assigned
        """
        if user.type is UserType.PROF and section.prof is None:
            section.prof = user
            return True
        else:
            return False

    @staticmethod
    def remove_prof_from_section(user: User, section: Section) -> bool:
        """
        Removes a Prof from a Section if there has been one assigned
        """
        if user.type is UserType.PROF and section.prof is not None:
            section.prof = None
            return True
        else:
            return False

    @staticmethod
    def assign_ta_to_section(user: User, section: Section, max_lab: int) -> bool:
        """
        Assigns a TA to a section and specifies the maximum number of lab sections the TA can be assigned
        for that particular section. Returns false if TA was already in the list of TAs.
        """
        qs = section.tas.all()
        if user not in qs:
            Assignment.objects.create(ta=user, section=section, max_labs=max_lab)
            return True
        else:
            return False

    @staticmethod
    def remove_ta_from_section(user: User, section: Section) -> bool:

        qs = Assignment.objects.filter(ta=user, section=section)

        if len(qs) == 1:
            qs[0].delete()
            return True
        else:
            return False

        # if user in map(lambda x: x.ta, iter(qs)):
        #     list(map(lambda x: x.delete(), iter(qs)))

    @staticmethod
    def assign_ta_to_lab(user: User, lab: Lab) -> bool:
        """
        Assigns a TA to a lab if one has not already been assigned.
        """
        if user.type is UserType.TA and lab.ta is None:
            lab.ta = user
            return True
        else:
            return False

    @staticmethod
    def remove_ta_from_lab(user: User, lab: Lab) -> bool:

        if user.type is UserType.TA and lab.ta is not None:
            lab.ta = None
            return True
        else:
            return False

    @staticmethod
    def check_ta_assign_number(user: User, section: Section) -> bool:
        """
        Checks TA lab assignments, returns True if TA can be assigned to another lab, false if quota is reached
        """
        max_labs = Assignment.objects.get(ta=user, section=section).max_labs
        labs_assigned = len(Lab.objects.filter(ta=user, section=section))

        response = False if max_labs <= labs_assigned else True
        return response


    @staticmethod
    def update_ta_assign_number(user: User, section: Section, new_max_lab: int) -> bool:
        """
        Updates the number of labs a TA can be assigned to, if the assignment exists
        """
        assignment = Assignment.objects.get(ta=user, section=section)

        if assignment is not None:
            assignment.max_labs = new_max_lab
            assignment.save()
            return True
        else:
            return False

    @staticmethod
    def get_ta_live_assignments(section: Section, lab_list: List[Tuple[int,int]]) -> bool:
        """
        Takes a list of tuples of (user id, actual # assigns) and checks the status against the database,
        determines if any updates needed, and does the update on each user.
        """
        pass
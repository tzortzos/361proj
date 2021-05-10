from TAScheduler.models import User, Section, Lab,Assignment


class AssignUtility:

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
    def remove_ta_from_section(user: User, section, Section) -> None:
        pass

    @staticmethod
    def assingn_ta_to_lab(user: User, lab: Lab) -> None:
        pass

    @staticmethod
    def remove_ta_from_lab(user: User, lab, Lab) -> None:
        pass

    @staticmethod
    def check_ta_assign_number(users: list[User]) -> int:
        pass

    @staticmethod
    def update_ta_assign_number(user) -> None:
        pass

    @staticmethod
    def assign_prof_to_section(user: User, section: Section) -> None:
        pass

    @staticmethod
    def remove_prof_from_section(user: User, section, Section) -> None:
        pass

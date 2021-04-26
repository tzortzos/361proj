from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabError
from django.test import Client


class LabsCreate(TASAcceptanceTestCase[LabError]):

    def setUp(self):
        self.client = Client()
        self.session = self.client.session

    def test_create_without_days_times(self):
        pass

    def test_create_full(self):
        pass

    def test_ta_redirects(self):
        pass

    def test_rejects_missing_code(self):
        pass

    def test_rejects_non_digit_code(self):
        pass

    def test_rejects_mislengthed_code(self):
        # Test that code lengths must be 3
        pass

    def test_rejects_missing_section(self):
        pass

    def test_rejects_professor_change_non_assignments(self):
        # A professor can edit lab sections, but only their assignments
        pass

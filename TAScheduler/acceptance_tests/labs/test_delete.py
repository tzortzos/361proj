from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import LabError
from django.test import Client


class LabsDelete(TASAcceptanceTestCase[LabError]):

    def setUp(self):
        self.client = Client()
        self.session = self.client.session

    def test_redirects_professor(self):
        pass

    def test_redirects_ta(self):
        pass

    def test_context_contains_lab(self):
        pass
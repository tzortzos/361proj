from TAScheduler.acceptance_tests.acceptance_base import TASAcceptanceTestCase
from TAScheduler.viewsupport.errors import TAError
from django.test import Client


class LabsCreate(TASAcceptanceTestCase[TAError]):

    def setUp(self):
        self.client = Client()
        self.session = self.client.session

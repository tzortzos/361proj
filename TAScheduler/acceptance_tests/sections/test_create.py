from django.shortcuts import reverse
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse
from django.db.models import ObjectDoesNotExist

from TAScheduler.models import User, UserType, Course, CourseSection
from TAScheduler.viewsupport.errors import SectionError
from TAScheduler.viewsupport.message import Message, MessageQueue

class CreateSection(TestCase):

    def setUp(self):
        pass

    def test_one(self):
        pass
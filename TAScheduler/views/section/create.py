from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from typing import List, Union

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.viewsupport.message import Message, MessageQueue
from TAScheduler.viewsupport.navbar import AdminItems


class SectionsCreate(View):
    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        pass

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        pass

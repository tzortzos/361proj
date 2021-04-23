from django.http import HttpRequest
from django.views import View
from django.shortcuts import render

from TAScheduler.viewsupport.message import MessageQueue, Message
from TAScheduler.viewsupport.navbar import AdminItems


class UserView(View):

    def get(self, request: HttpRequest):
        return render(request, 'pages/example.html', context={
            'navbar_items': AdminItems.HOME.items_iterable_except(),
            'messages': MessageQueue.drain(request.session),
        })

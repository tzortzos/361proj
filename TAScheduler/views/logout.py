from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse

from TAScheduler.viewsupport.message import Message, MessageQueue


class Logout(View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        try:
            del request.session['user_id']
            MessageQueue.push(request.session, Message('Successfully logged out'))
        except KeyError:
            # We do not actually care if there was no user, we simply do not send the logged out message
            pass

        return redirect(reverse('index'))

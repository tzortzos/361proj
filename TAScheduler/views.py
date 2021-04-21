from django.shortcuts import render
from django.views import View

from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.errors import PageError, LoginError

# Create your views here.

class Login(View):
    def get(self, request):
        return render(request, 'pages/login.html', {
            'error': LoginError(PageError('This is a password error'), LoginError.Place.USERNAME)
        })

    def post(self, request):
        print('User Tried to log in')
        print(request)
        pass


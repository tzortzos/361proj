from django.shortcuts import render
from django.views import View

from TAScheduler.viewsupport.navbar import AdminItems
from TAScheduler.viewsupport.errors import PageError, LoginError
from TAScheduler.models import User, UserType

# Create your views here.
class Index(View):

    def get(self, request):
        return render(request, 'pages/example.html', context={
            'navbar_items': AdminItems.HOME.items_iterable_except(),
            'user_name': 'Josiah Hilden'
        })

    def post(self, request):
        return render(request, 'pages/index.html')

class Login(View):
    def get(self, request):
        return render(request, 'pages/login.html', {
            'error': LoginError(PageError('This is a password error'), LoginError.Place.USERNAME)
        })

    def post(self, request):
        print('User Tried to log in')
        print(request)
        pass

class CourseEdit(View):
    def get(self, request):
        return render(request, 'pages/create_course.html', {
            'navbar_items': AdminItems.items_iterable(),
        })


class CreateUser(View):
    def get(self, request):
        self = User.objects.get(user_id=3)
        return render(request, 'pages/create_user.html', {
            'navbar_items': AdminItems.items_iterable(),
            'self': self,
        })

class EditUser(View):
    def get(self, request, user_id: int):
        self = User.objects.get(user_id=3)
        return render(request, 'pages/create_user.html', {
            'navbar_items': AdminItems.items_iterable(),
            'self': self,
            'edit': self,
        })

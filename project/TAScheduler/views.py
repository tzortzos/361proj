from django.shortcuts import render
from django.views import View

from TAScheduler.viewsupport.navbar import AdminItems

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
        return render(request, 'pages/login.html')

    def post(self, request):
        print('User Tried to log in')
        print(request)
        pass
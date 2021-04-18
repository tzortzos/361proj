from django.shortcuts import render
from django.views import View


# Create your views here.
class Index(View):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        return render(request, 'index.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        print('User Tried to log in')
        print(request)
        pass
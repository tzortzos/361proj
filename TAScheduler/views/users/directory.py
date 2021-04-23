from django.shortcuts import redirect, reverse, render
from django.views import View

class UserDirectory(View):
    def get(self, request):
        return render(request, 'pages/index.html')

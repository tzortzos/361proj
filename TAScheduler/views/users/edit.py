from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, reverse


# Obviously just a stub, needed to make login acceptance tests pass.
class UserEdit(View):
    """
    Represents the user edit page, which will only be visible if editing self or logged in user is admin.
    """

    def get(self, request: HttpRequest, user_id: int):
        return render(request, 'pages/index.html')

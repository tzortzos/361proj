from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Union
import uuid

from TAScheduler.ClassDesign.LoginUtility import LoginUtility
from TAScheduler.ClassDesign.UserAPI import UserAPI, UserType
from TAScheduler.viewsupport.navbar import AdminItems

class UserCreate(View):

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        try:
            user_id= request.session['user_id']
        except KeyError:
            return redirect(reverse('login'))

        user = LoginUtility.get_user_and_validate_by_user_id(user_id)

        # check user is admin
        if UserAPI.check_user_type(user) is not UserType.ADMIN:
            return redirect('index')

        tmp_pass = str(uuid.uuid4())[:8]

        return render(request, 'pages/create_user.html', {
            'self': user,
            'navbar_items': AdminItems.items_iterable(),
            'new_user_pass': tmp_pass
        })



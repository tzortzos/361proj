from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse

from TAScheduler.ClassDesign.UserAPI import UserType, UserAPI

from TAScheduler.viewsupport.errors import LoginError, LoginPlace
from TAScheduler.viewsupport.message import MessageQueue


class Login(View):
    """
    Represents the login page for users, template has the following context options:
    - error: Optional[LoginError] : Mark a field in the form as being in an error state and
      show a message to the user indicating why
    - user_name: Optional[str] : Pre-fill the username field with a username, to be used in
      the case of a failed login
    """

    def get(self, request: HttpRequest):
        u = request.session.get('user_id', None) is None

        if u:
            return render(request, 'pages/login.html', {
                'messages': MessageQueue.drain(request.session),
            })
        else:
            return redirect(reverse('index'))

    def post(self, request: HttpRequest):

        r_username = request.POST.get('username', '')
        r_password = request.POST.get('password', '')



        # Username Empty
        if len(r_username) == 0:
            return render(request, 'pages/login.html', {
                'error': LoginError('You must provide a username', LoginPlace.USERNAME)
            })

        # Username too long
        if len(r_username) > 20:
            return render(request, 'pages/login.html', {
                'error': LoginError('That Username is too Long', LoginPlace.USERNAME)
            })

        # Password Empty
        if len(r_password) == 0:
            return render(request, 'pages/login.html', {
                'error': LoginError('You must provide a password', LoginPlace.PASSWORD),
                'user_name': r_username
            })

        # Password too short
        if len(r_password) < 8:
            return render(request, 'pages/login.html', {
                'error': LoginError('A password must be at least 8 characters in length', LoginPlace.PASSWORD),
                'user_name': r_username,
            })

        user = UserAPI.get_user_by_univ_id(r_username)

        if user is None:
            # No such user exists
            return render(request, 'pages/login.html', {
                'error': LoginError('No such user', LoginPlace.USERNAME),
                'user_name': r_username,
            })

        if user.password != r_password:
            # The password does not match for the user
            return render(request, 'pages/login.html', {
                'error': LoginError('Incorrect Password', LoginPlace.PASSWORD),
                'user_name': r_username,
            })
        else:
            # Login successful
            request.session['user_id'] = user.id

            if user.password_tmp:
                return redirect(reverse('users-edit', args=[user.id]))

            return redirect(reverse('index'))

from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse

from TAScheduler.ClassDesign.UserAPI import UserType, UserAPI

from TAScheduler.viewsupport.errors import PageError, LoginError


class Login(View):
    """
    Represents the login page for users, template has the following context options:
    - error: Optional[LoginError] : Mark a field in the form as being in an error state and
      show a message to the user indicating why
    - user_name: Optional[str] : Pre-fill the username field with a username, to be used in
      the case of a failed login
    """

    def get(self, request: HttpRequest):
        try:
            # In the case where the user is already logged in,
            # we redirect them to their homepage
            _ = request.session['user_id']
            return redirect(reverse('index'))

        except KeyError:
            # Otherwise we render the default login page
            return render(request, 'pages/login.html')

    def post(self, request: HttpRequest):

        try:
            r_username = request.POST['username']
        except KeyError:
            # No Username Provided
            r_username = None

        # Username Empty
        if r_username is None or len(r_username) == 0:
            return render(request, 'pages/login.html', {
                'error': LoginError(PageError('You must provide a username'), LoginError.Place.USERNAME)
            })

        # Username too long
        if len(r_username) > 20:
            return render(request, 'pages/login.html', {
                'error': LoginError(PageError('That Username is too Long'), LoginError.Place.USERNAME)
            })

        try:
            r_password = request.POST['password']
        except KeyError:
            # No Password Provided
            r_password = None

        # Password Empty
        if r_password is None or len(r_password) == 0:
            return render(request, 'pages/login.html', {
                'error': LoginError(PageError('You must provide a password'), LoginError.Place.PASSWORD),
                'user_name': r_username
            })

        # Password too short
        if len(r_password) < 8:
            return render(request, 'pages/login.html', {
                'error': LoginError(PageError('A password must be at least 8 characters in length'), LoginError.Place.PASSWORD),
                'user_name': r_username,
            })

        user = UserAPI.get_user_by_univ_id(r_username)
        if user is None:
            # No such user exists
            return render(request, 'pages/login.html', {
                'error': LoginError(PageError('No such user'), LoginError.Place.USERNAME),
                'user_name': r_username,
            })

        if user.password != r_password:
            # The password does not match for the user
            return render(request, 'pages/login.html', {
                'error': LoginError(PageError('Incorrect Password'), LoginError.Place.PASSWORD),
                'user_name': r_username,
            })
        else:
            # Login successful
            request.session['user_id'] = user.user_id

            if user.tmp_password:
                # This is the first login so the user should be
                return redirect(reverse('user-edit', args=(user.user_id,)))
            else:
                return redirect(reverse('index'))

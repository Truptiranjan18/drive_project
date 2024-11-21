# myproject/middleware/login_middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class LoginMiddleware:
    """
    Custom middleware to check if the user is logged in.
    Redirects the user to the login page if not logged in.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not logged in and the request is not for the login page
        if not request.user.is_authenticated and not request.path.startswith(reverse('login')):
            return redirect('login')  # Redirect to login page
        response = self.get_response(request)
        return response

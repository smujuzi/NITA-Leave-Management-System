from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_function


"""
If the decorator is expecting parameters, those parameters will be represented at the top of the nest,
Decorator has the class-based view while the wrapper function has the parameters of the class-based view
"""


def admin_redirect(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_staff:
            print("This is a MEMBER OF STAFF")
            return redirect('adminHome')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

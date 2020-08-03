from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from UsersAuth.models import Account
from django.contrib.auth import login, authenticate, logout
from UsersAuth.forms import RegistrationForm, AccountAuthenticationForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
#from .decorators import *

from django.contrib import messages 



#Enables User to register an account
class RegisterView(View):
    template_name = 'UsersAuth/register.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, self.template_name, context)

    @staticmethod
    def create_institution(request, company_form):
        email = company_form.cleaned_data.get('email')
        raw_password = company_form.cleaned_data.get('password1')
        account = authenticate(email=email, password=raw_password)
        login(request, account)
        company_form.save()
        return redirect('employeeDashboard:apply')

    def post(self, request, *args, **kwargs):
        context = {}
        company_form = RegistrationForm(request.POST)


        if company_form.is_valid():
            company_form.save()

            email = company_form.cleaned_data.get('email')
            raw_password = company_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('employeeDashboard:apply')
        else:
            context['registration_form'] = company_form
            return render(request, self.template_name, context)


# Enables to login into the system
def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("employeeDashboard:apply")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("employeeDashboard:apply")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "UsersAuth/login.html", context)
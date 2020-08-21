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
from datetime import timedelta, datetime
from math import floor
from dateutil.relativedelta import relativedelta

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

            #******TESTING**************

            registered_user = company_form.save(commit=False)

            if registered_user.role == "Line Manager":
                registered_user.is_staff = True
                registered_user.is_line_manager = True

            elif registered_user.role == "Director":
                registered_user.is_staff = True
                registered_user.is_director = True

            elif registered_user.role == "Executive Director":
                registered_user.is_staff = True
                registered_user.is_admin = True
                registered_user.is_executive_director = True

            registered_user.save()
            # ******TESTING**************
            #company_form.save()

            email = company_form.cleaned_data.get('email')
            raw_password = company_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('employeeDashboard:apply')
        else:
            context['registration_form'] = company_form
            return render(request, self.template_name, context)


# Enables user to login into the system
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

    LeaveAccumulated(request)
    context['login_form'] = form

    return render(request, "UsersAuth/login.html", context)

#Continously checks if a month has passed in order to give employees leave days
def LeaveAccumulated(request):
    all_records = Account.objects.all()
    for employee in all_records:

        days_since_joining = (datetime.today() - employee.start_of_month_tracker).days


        # Checks whether the employee has a regular role
        if employee.role == "Employee":
            leave_days = floor(days_since_joining / 30) * 2 #Two leave days are added each month for regular employees
            #Once "days_since_joining" = 30 this means
            # a month has passed and therefore leave days
            # shall be added to the user's account

            if leave_days != 0 and leave_days % 2 == 0: #Checks if Leave days have been accumulated

                employee.OutstandingLeaveDays = employee.OutstandingLeaveDays + leave_days
                employee.start_of_month_tracker = datetime.today()
                employee.save()

        # This means the employee is a Line Manager, Director or Executive Director
        else:
            leave_days = floor(days_since_joining / 30) * 3  #Three leave days are added each month for management and above.
            # Once "days_since_joining" = 30 this means
            # a month has passed and therefore leave days
            # shall be added to the user's account

            if leave_days != 0 and leave_days % 3 == 0:  # Checks if Leave days have been accumulated

                employee.OutstandingLeaveDays = employee.OutstandingLeaveDays + leave_days
                employee.start_of_month_tracker = datetime.today()
                employee.save()

    #CODE FOR TESTING LEAVE ACCUMULATED
    # testing future dates
    # future_date = datetime.today() + relativedelta(months=7)
    # days_btn_now_and_future = (future_date - datetime.today()).days
    # print("Future Date")
    # print(future_date)
    # print("Days between now and future")
    # print(days_btn_now_and_future)
    # current_leave_days = 2
    # leave_days_accumulated = floor(days_btn_now_and_future / 30) * 2
    # print("Leave Days")
    # print(leave_days_accumulated)
    #
    # if leave_days % 2 == 0:
    #     current_leave_days = current_leave_days + leave_days_accumulated
    #     print("Current = ")
    #     print(current_leave_days)
from django.shortcuts import render, redirect
from adminDashboard.models import *
from employeeDashboard.models import *
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import LeaveForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import inspect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import *
from UsersAuth.models import Account

decorators = [admin_redirect]

@method_decorator(decorators, 'dispatch') # Determines whether an employee or privileged user(manager or director) has logged in
class ApplyLeaveView(View):

    template_name = 'leaves_form.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user.first_name + " " + request.user.last_name
        remaining_leave = 1000

        director = Director.objects.filter(name=current_user)  # Filters for logged in user in list of Directors
        line_manager = LineManager.objects.filter(name=current_user)  # Filters for logged in user in list of Line Managers
        executive_director = ExecutiveDirector.objects.filter(name=current_user)  # Filters for logged in user in list of Executive Director

        context = {}

        try:
            applied_for_leave = Leaves.objects.filter(name=current_user).latest('id').id #Check if a leave request has been
                                                                                        # made before by getting previous ID
        except Leaves.DoesNotExist:
            applied_for_leave = None
            leave_form = LeaveForm(

                initial={
                    "name": request.user.first_name + " " + request.user.last_name,
                    "OutstandingLeaveDays": 24,
                }
            )

        if applied_for_leave:

          #Checks if the user has already made a previous leave application. If so, remaining days are calculated
            prev = Leaves.objects.filter(name=current_user).latest('id').id
            remaining_leave = Leaves.objects.get(pk=prev)

            leave_form = LeaveForm(

                initial={
                    "name": request.user.first_name + " " + request.user.last_name,
                    "OutstandingLeaveDays": remaining_leave.OutstandingLeaveDays,


                }
            )
            remaining_leave = remaining_leave.OutstandingLeaveDays

        elif request.user.is_staff:
            leave_form = LeaveForm(initial={
                "name": request.user.first_name + " " + request.user.last_name,
                "OutstandingLeaveDays": 36,

            })


        out_of_leave = 0 #Used to ensure that "Remaining leave" doesn't go lower than this value
        context['leave_form'] = leave_form
        context['out_of_leave'] = out_of_leave
        context['remaining_leave'] = remaining_leave

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}

        leave_form = LeaveForm(request.POST, request.FILES)

        if leave_form.is_valid():
            leave_user = leave_form.save(commit=False)
            result = leave_user.OutstandingLeaveDays - leave_user.NumberOfDaystaken #Calculates outstading leave days

            if result < 0:
                messages.warning(request, f'YOU HAVE EXCEEDED YOUR ALLOCATED NUMBER OF LEAVE DAYS')
                return redirect('employeeDashboard:apply')

            leave_user.OutstandingLeaveDays = result
            leave_user.save()


            # Finds the line manager of the department
            hold = leave_user.empDepartment
            department = LineManager.objects.get(Departments_under=hold)
            line_manager = department.name
            split_line_manager = line_manager.split(' ')
            email_line_manager = Account.objects.get(last_name=split_line_manager[1], first_name=split_line_manager[0])
            print("Email =")
            print(email_line_manager.email)
            #Sends email to line manager requesting for Leave
            send_mail(
                subject="Leave Request",
                message="Hello "+line_manager+" ,\n I am requesting to go for leave. "
                                              "\n Please go to the NITA Leave Management Portal to action this request.",
                from_email=request.user.email,
                recipient_list=[email_line_manager.email]
            )

            return redirect('employeeDashboard:history')
        else:
            context['leave_form'] = leave_form
            return render(request, self.template_name, context)




def leave_history(request):  #Displays all leave requests a user has made
    current_user = request.user.first_name + " " + request.user.last_name

    leave_history = Leaves.objects.filter(name=current_user)

    context = {
        'leave_history': leave_history
    }
    return render(request, 'history.html', context)


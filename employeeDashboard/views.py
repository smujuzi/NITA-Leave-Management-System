from django.shortcuts import render, get_object_or_404, redirect
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

        context = {}

        leave_form = LeaveForm(initial={
            "name": request.user.first_name + " " + request.user.last_name,
            "OutstandingLeaveDays": request.user.OutstandingLeaveDays,

        })

        if request.user.OutstandingLeaveDays > 30:
            messages.warning(request, f'YOU HAVE TOO MANY LEAVE DAYS! PLEASE APPLY FOR LEAVE TO UNBLOCK THE PORTAL FOR YOUR SUPERVISOR')

        out_of_leave = 0 #Used to ensure that "Remaining leave" doesn't go lower than this value
        context['leave_form'] = leave_form
        context['out_of_leave'] = out_of_leave
        context['remaining_leave'] = remaining_leave

        return render(request, self.template_name, context)

    @staticmethod
    def email_leave_request(request):

        if request.user.role == "Employee":

            line_manager = Account.objects.get(role="Line Manager", department=request.user.department)




            # Sends email to line manager requesting for Leave
            send_mail(
                subject="Leave Request",
                message="Hello " + line_manager.first_name + " " + line_manager.last_name + " ,\n I am requesting to go for leave. "
                                                  "\n Please go to the NITA Leave Management Portal to action this request.",
                from_email=request.user.email,
                recipient_list=[line_manager.email]
            )

        elif request.user.role == "Line Manager":

            director = Account.objects.get(role="Director", directorate=request.user.directorate)
            # Sends email to director requesting for Leave
            send_mail(
                subject="Leave Request",
                message="Hello " + director.first_name + " " + director.last_name + " ,\n I am requesting to go for leave. "
                                                     "\n Please go to the NITA Leave Management Portal to action this request.",
                from_email=request.user.email,
                recipient_list=[director.email]
            )
        elif request.user.role == "Director":

            executive_director = Account.objects.get(role="Executive Director")
            # Sends email to executive director requesting for Leave
            send_mail(
                subject="Leave Request",
                message="Hello " + executive_director.first_name + " " + executive_director.last_name + " ,\n I am requesting to go for leave. "
                                                     "\n Please go to the NITA Leave Management Portal to action this request.",
                from_email=request.user.email,
                recipient_list=[executive_director.email]
            )



    def post(self, request, *args, **kwargs):
        context = {}


        leave_form = LeaveForm(request.POST, request.FILES)

        if leave_form.is_valid():
            leave_user = leave_form.save(commit=False)
            result = leave_user.OutstandingLeaveDays - leave_user.NumberOfDaystaken #Calculates outstading leave days

            if result < 0:
                messages.warning(request, f'YOU HAVE EXCEEDED YOUR ALLOCATED NUMBER OF LEAVE DAYS')
                return redirect('employeeDashboard:apply')

            edit_account_leave_days = Account.objects.get(email=request.user.email)
            edit_account_leave_days.OutstandingLeaveDays = result
            edit_account_leave_days.save()

            leave_user.OutstandingLeaveDays = result

            if request.user.role == "Director":
                leave_user.Approval_by_Line_Manager = "Approved"

            if request.user.role == "Executive Director":
                leave_user.Approval_by_Line_Manager = "Approved"
                leave_user.Approval_by_Director = "Approved"

            leave_user.save()

            self.email_leave_request(request)


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

def cancel_request(request , *args, **kwargs):
    leave_id = kwargs.get('pk')
    selected_leave_request = get_object_or_404(Leaves, pk=leave_id)
    selected_leave_request.Approval_by_Line_Manager = 'Pending'
    selected_leave_request.Approval_by_Director = 'Pending'
    selected_leave_request.Approval_by_Executive_Director = 'Pending'
    selected_leave_request.cancellation_status = True

    selected_leave_request.save()


    current_user = request.user.first_name + " " + request.user.last_name
    leave_history = Leaves.objects.filter(name=current_user)

    context = {
        'leave_history': leave_history
    }
    return render(request, 'history.html', context)



from django.shortcuts import render, redirect
from adminDashboard.models import *
from employeeDashboard.models import *
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import LeaveForm
from django.urls import reverse_lazy
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import inspect


class ApplyLeaveView(View):

    template_name = 'leaves_form.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user.first_name + " " + request.user.last_name
        context = {}

        print("Arrive here!")

        try:
            applied_for_leave = Leaves.objects.filter(name=current_user).latest('id').id
        except Leaves.DoesNotExist:
            applied_for_leave = None

        print("Applied for Leave = ")
        print(applied_for_leave)

        if applied_for_leave:
        #if Leaves.objects.filter(name=current_user).latest('id').id:   #Checks if the user has already made a previous leave application. If so, remaining days are calculated
            print("Got here!")
            prev = Leaves.objects.filter(name=current_user).latest('id').id
            print("Last ID = ")
            print(prev)
            remain = Leaves.objects.get(pk=prev)
            print("Previous remaining days = ")
            print(remain.OutstandingLeaveDays)

            leave_form = LeaveForm(

                initial={
                    "name": request.user.first_name + " " + request.user.last_name,
                    "OutstandingLeaveDays": remain.OutstandingLeaveDays

                }
            )
        else:

            leave_form = LeaveForm(

                initial={
                    "name": request.user.first_name + " " + request.user.last_name,
                    "OutstandingLeaveDays": 30

                }
            )

        context['leave_form'] = leave_form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}

        print("Inside Post")

        leave_form = LeaveForm(request.POST, request.FILES)

        if leave_form.is_valid():
            leave_user = leave_form.save(commit=False)
            result = leave_user.OutstandingLeaveDays - leave_user.NumberOfDaystaken
            leave_user.OutstandingLeaveDays = result
            leave_user.save()

            # Finding the line manager of the department
            hold = leave_user.empDepartment
            department = LineManager.objects.get(Departments_under=hold)
            line_manager = department.name
            split_line_manager = line_manager.split(' ')
            email_line_manager = User.objects.get(last_name=split_line_manager[1], first_name=split_line_manager[0])
            print("Email =")
            print(email_line_manager.email)

            send_mail(
                subject="Leave Request",
                message="Hello "+line_manager+" ,\n I am requesting to go for leave. "
                                              "\n Please go to the NITA Leave Management Portal to action this request.",
                from_email=request.user.email,
                recipient_list=[email_line_manager.email]
            )

            return redirect('history')
        else:
            context['leave_form'] = leave_form
            return render(request, self.template_name, context)



@login_required
def leave_history(request):
    current_user = request.user.first_name + " " + request.user.last_name

    leave_history = Leaves.objects.filter(name=current_user)

    print(request.user.email)
    print("Hello " + current_user)

    context = {
        'leave_history': leave_history
    }
    return render(request, 'history.html', context)


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, reverse
from django.http import HttpResponse
from adminDashboard.forms import ApprovalForm
from adminDashboard.models import *

from leaveproject.decorators import *
from employeeDashboard.models import Leaves
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User

from adminDashboard.models import Approve

# Create your views here.

'''
class Leave_tracker(View):
    def begining_phase():
        if(lm_status == "rejected"):
            print('application rejected ')
        else:
            print('application forwarded to Director')

    def middle_phase():
        if(dr_status == "rejected"):
            print('application rejected by the Director')
        else:
            print('application fowarde to Executive Director')

    def end_phase():
        if(ed_status == "rejected"):
            print('application rejected by the Executive Director')
        else:
            print('application approved by the Executive Director')

'''


def admin_view(request):
    context = {}

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    print("Inside Admin!")

    if executive_director:  # Checks if logged in user is a director
        print("This is the EXECUTIVE DIRECTOR!")
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    if director:  # Checks if logged in user is a director
        print("This is a DIRECTOR!")
        director = Director.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDirector=director).filter(Q(Approval_by_Line_Manager='Pending')
                                                                            | Q(Approval_by_Director='Pending')
                                                                            | Q(Approval_by_Executive_Director='Pending'
                                                                                )).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(empDirector=director, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDirector=director).filter(Q(Approval_by_Line_Manager='Rejected')
                                                                            | Q(Approval_by_Director='Rejected')
                                                                            | Q(Approval_by_Executive_Director='Rejected'
                                                                                )).order_by('DateApplied')

    if line_manager:  # Checks if logged in user is a manager
        print("This is a LINE MANAGER!")
        line_manager = LineManager.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
            | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Rejected') | Q(Approval_by_Director='Rejected')
            | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')



    status = Leaves.objects.all()

    value = pending_leave.count()
    valuea = approved_leave.count()
    valuer = rejected_leave.count()
    print(value)
    print(valuea)
    print(valuer)

    context['status'] = status
    context['pending_leave'] = pending_leave
    context['approved_leave'] = approved_leave
    context['rejected_leave'] = rejected_leave

    return render(request, 'adminDashboard/index.html', context)


@login_required(login_url='login')
@admin_redirect
def dashboard(request):
    return render(request, 'adminDashboard/dashboard.html')


def notifications(request):
    return render(request, 'adminDashboard/notifications.html')


def approved(request):
    context = {}
    approved_leave = Leaves.objects.filter(name="")

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    print("Below admins")

    if executive_director:  # Checks if logged in user is a director
        print("This is the EXECUTIVE DIRECTOR!")
        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

    if director:  # Checks if logged in user is a director
        print("This is a DIRECTOR!")
        director = Director.objects.get(name=name)
        approved_leave = Leaves.objects.filter(empDirector=director, Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

    if line_manager:  # Checks if logged in user is a manager
        print("This is a LINE MANAGER!")
        line_manager = LineManager.objects.get(name=name)
        approved_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

    context['approved_leave'] = approved_leave

    return render(request, 'adminDashboard/leavemanagement/approvedleaves.html', context)


def pending(request):
    context = {}

    pending_leave = Leaves.objects.filter(name="")

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    print("Below admins")

    if executive_director:  # Checks if logged in user is a director
        print("This is the EXECUTIVE DIRECTOR!")
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

    if director:  # Checks if logged in user is a director
        print("This is a DIRECTOR!")
        director = Director.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDirector=director).filter(Q(Approval_by_Line_Manager='Pending')
                                                                            | Q(Approval_by_Director='Pending')
                                                                            | Q(Approval_by_Executive_Director='Pending'
                                                                                )).order_by('DateApplied')

    if line_manager:  # Checks if logged in user is a manager
        print("This is a LINE MANAGER!")
        line_manager = LineManager.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
            | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

    context['pending_leave'] = pending_leave

    return render(request, 'adminDashboard/leavemanagement/pendingleaves.html', context)


def rejected(request):
    context = {}

    rejected_leave = Leaves.objects.filter(name="")

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    print("Below admins")

    if executive_director:  # Checks if logged in user is a director
        print("This is the EXECUTIVE DIRECTOR!")
        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected') | Q(Approval_by_Director='Rejected')
                                              | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    if director:  # Checks if logged in user is a director
        print("This is a DIRECTOR!")
        director = Director.objects.get(name=name)
        rejected_leave = Leaves.objects.filter(empDirector=director).filter(Q(Approval_by_Line_Manager='Rejected')
                                                                            | Q(Approval_by_Director='Rejected')
                                                                            | Q(Approval_by_Executive_Director='Rejected'
                                                                                )).order_by('DateApplied')

    if line_manager:  # Checks if logged in user is a manager
        print("This is a LINE MANAGER!")
        line_manager = LineManager.objects.get(name=name)
        rejected_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Rejected') | Q(Approval_by_Director='Rejected')
            | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    context['rejected_leave'] = rejected_leave

    return render(request, 'adminDashboard/leavemanagement/rejectedleaves.html', context)


def history(request):
    context = {}
    print("Inside History!")

    all_leave = Leaves.objects.all()
    status = Leaves.objects.all()

    print("All Leave")
    print(all_leave)

    pending_leave = Leaves.objects.filter(Approval_by_Line_Manager='Pending', Approval_by_Director='Pending',
                                          Approval_by_Executive_Director='Pending').order_by('DateApplied')

    approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                           Approval_by_Executive_Director='Approved').order_by('DateApplied')

    rejected_leave = Leaves.objects.filter(Approval_by_Line_Manager='Rejected', Approval_by_Director='Rejected',
                                           Approval_by_Executive_Director='Rejected').order_by('DateApplied')

    context['pending_leave'] = pending_leave
    context['approved_leave'] = approved_leave
    context['rejected_leave'] = rejected_leave
    context['all_leave'] = all_leave

    return render(request, 'adminDashboard/alleaves.html', context)


class LeaveListView(ListView):
    template_name = "adminDashboard/leavemanagement/allleaves.html"

    def get(self, request, *args, **kwargs):
        print("Inside LeaveListView Get")

        context = {}
        all_leave = Leaves.objects.filter(name="")

        name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

        director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
        line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
        executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
        print("Below admins")

        if executive_director:  # Checks if logged in user is a director
            print("This is the EXECUTIVE DIRECTOR!")
            all_leave = Leaves.objects.all()

        if director:  # Checks if logged in user is a director
            print("This is a DIRECTOR!")
            director = Director.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDirector=director)

        if line_manager:  # Checks if logged in user is a manager
            print("This is a LINE MANAGER!")
            line_manager = LineManager.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under)

        context['all_leave'] = all_leave

        return render(request, self.template_name, context)


class LeaveDetailView(DetailView):
    print("Inside Leave")

    template_name = "adminDashboard/leavedetails.html"

    def get(self, request, *args, **kwargs):
        print("Inside Leave Get")

        context = {}
        all_leave = Leaves.objects.filter(name="")

        name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

        director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
        line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
        executive_director = ExecutiveDirector.objects.filter(
            name=name)  # Filters for logged in user in list of Executive Director
        print("Below admins")

        if executive_director:  # Checks if logged in user is a director
            print("This is the EXECUTIVE DIRECTOR!")
            all_leave = Leaves.objects.all()

        if director:  # Checks if logged in user is a director
            print("This is a DIRECTOR!")
            director = Director.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDirector=director)

        if line_manager:  # Checks if logged in user is a manager
            print("This is a LINE MANAGER!")
            line_manager = LineManager.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under)

        context['all_leave'] = all_leave

        print("At the bottom!")
        return render(request, self.template_name, context)


class LeaveUpdateView(UpdateView):
    print("Inside Update")

    # template_name = "adminDashboard/leavedetails.html"
    template_name = "adminDashboard/status_update.html"

    def get(self, request, *args, **kwargs):
        print("Inside Update Get")
        context = {}

        approval_form = ApprovalForm()

        context['approval_form'] = approval_form

        print("At the bottom!")
        return render(request, self.template_name, context)

    @staticmethod
    def approved(selected_employee, sender):

        name = selected_employee.name
        split_line_name = name.split(' ')
        email_name = User.objects.get(last_name=split_line_name[1], first_name=split_line_name[0])
        print("Email =")
        print(email_name.email)

        send_mail(
            subject="Leave Request",
            message="Hello " + name + " ,\n I have approved this leave request. "
                                      "\n Please go to the NITA Leave Management Portal to action the next phase of this request.",
            from_email=sender,
            recipient_list=[email_name.email]
        )

    @staticmethod
    def rejected(selected_employee, sender):
        employee = selected_employee.name
        split_employee = employee.split(' ')
        email_employee = User.objects.get(last_name=split_employee[1], first_name=split_employee[0])
        print("Email =")
        print(email_employee.email)

        send_mail(
            subject="Leave Request",
            message="Hello " + employee + " ,\n Sorry, your request to take leave has been rejected. ",
            from_email=sender,
            recipient_list=[email_employee.email]
        )

    def post(self, request, *args, **kwargs):

        leave_id = self.kwargs.get('pk')
        print("Leave ID = ")
        print(leave_id)

        selected_employee = get_object_or_404(Leaves, pk=leave_id)
        print("Employee name = ")
        print(selected_employee.name)

        # *****************************
        name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in
        print("Staff Name is")
        print(name)

        director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
        line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
        executive_director = ExecutiveDirector.objects.filter(
            name=name)  # Filters for logged in user in list of Executive Director

        # *****************************

        print("Inside Post")
        context = {}
        approval_form = ApprovalForm(request.POST)
        all_leave = Leaves.objects.all()

        context['all_leave'] = all_leave

        if approval_form.is_valid():
            post = approval_form.save(commit=False)
            post.save()
            print("Leave Status = ")
            print(post.leave_status)
            print("All Leave = ")
            print(all_leave)

            # Edit Leave Object
            if executive_director:  # Checks if logged in user is a director
                print("This is the EXECUTIVE DIRECTOR!")
                # Change Director field in leave model to approved
                selected_employee.Approval_by_Executive_Director = post.leave_status
                selected_employee.save()

                if post.leave_status == "Approved":
                    self.approved(selected_employee, request.user.email)
                elif post.leave_status == "Rejected":
                    self.rejected(selected_employee, request.user.email)

            if director:  # Checks if logged in user is a director
                print("This is a DIRECTOR!")
                # Change Director field in leave model to approved
                selected_employee.Approval_by_Director = post.leave_status
                selected_employee.save()
                # Need to send email to Executive Director to action Leave.
                if post.leave_status == "Approved":
                    ed = get_object_or_404(ExecutiveDirector)
                    self.approved(ed, request.user.email)
                elif post.leave_status == "Rejected":
                    self.rejected(selected_employee, request.user.email)

            if line_manager:  # Checks if logged in user is a manager
                print("This is a LINE MANAGER!")
                # Change Line Manager field in leave model to approved
                selected_employee.Approval_by_Line_Manager = post.leave_status
                selected_employee.save()
                # Need to send email to Head of Directorate to action Leave.
                # Finding the Director of the directorate
                if post.leave_status == "Approved":
                    self.approved(selected_employee.empDirector, request.user.email)
                elif post.leave_status == "Rejected":
                    self.rejected(selected_employee, request.user.email)

            print("NEW LEAVE STATUS EXECUTIVE DIRECTOR")
            print(selected_employee.Approval_by_Executive_Director)
            print("NEW LEAVE STATUS DIRECTOR")
            print(selected_employee.Approval_by_Director)
            print("NEW LEAVE STATUS LINE MANAGER")
            print(selected_employee.Approval_by_Line_Manager)

            return redirect(reverse("adminDashboard:LeaveDetailView"))



        else:
            context['approval_form'] = approval_form
            return render(request, self.template_name, context)

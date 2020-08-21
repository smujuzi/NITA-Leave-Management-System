from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, reverse
from django.http import HttpResponse
from adminDashboard.forms import ApprovalForm, SalaryForm
from adminDashboard.models import *
from UsersAuth.models import Account
from django.contrib import messages
from django.views import View


from employeeDashboard.models import Leaves
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from xlwt import Workbook
import tempfile
import os
import datetime

from .filters import LeaveFilter

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

def exceed_thirty(department, request):
    emp_over_thirty = Account.objects.filter(department=department.name, OutstandingLeaveDays__gt=30)

    director = Account.objects.get(role="Director", directorate=department.directory)

    hr = Account.objects.get(role="Line Manager", department="Human Resources")

    if emp_over_thirty:
        print("These people have an excess of 30 days leave. Please advise them to take leave")
        for emp in emp_over_thirty:
            print(emp.first_name)
            print(emp.OutstandingLeaveDays)
            send_mail(
                subject="Excess Leave Days",
                message="Hello " + emp.first_name + " " +emp.last_name + " ,\n You have surpassed the 30 outstanding leave days threshold."
                                          "\n Please go to the NITA Leave Management Portal and make a leave request to unblock your supervisor's portal.",
                from_email=hr.email,
                recipient_list=[emp.email, director.email]
            )

    return emp_over_thirty

def exceed_thirty_d(directorate, request):
    emp_over_thirty = Account.objects.filter(directorate=directorate.name, OutstandingLeaveDays__gt=30, role="Line Manager")

    executive_director = Account.objects.get(role="Executive Director")

    hr = Account.objects.get(role="Line Manager", department="Human Resources")

    if emp_over_thirty:
        print("These people have an excess of 30 days leave. Please advise them to take leave")
        for emp in emp_over_thirty:
            print(emp.first_name)
            print(emp.OutstandingLeaveDays)
            send_mail(
                subject="Excess Leave Days",
                message="Hello " + emp.first_name + " " +emp.last_name + " ,\n You have surpassed the 30 outstanding leave days threshold."
                                          "\n Please go to the NITA Leave Management Portal and make a leave request to unblock your supervisor's portal.",
                from_email=hr.email,
                recipient_list=[emp.email, executive_director.email]
            )

    return emp_over_thirty





#Creates Excel document of all Leave Requests

def convert_date(date_obj):
    return date_obj.strftime("%a / %d /%m/ %Y")


def export_members_excel(request):
    logs = Leaves.objects.all().order_by('-DateApplied')  # prepend "-" to order the logs in descending order using date
    data = [[obj.name, obj.empDirectorate.name, obj.empDepartment.name, obj.LeaveType, convert_date(obj.StartDate), convert_date(obj.EndDate), obj.OutstandingLeaveDays] for obj in logs]

    headers = ['Employee Name', 'Directorate', 'Department', 'Leave Type', 'Start Date', 'End Date', 'Remaining Leave Days']
    filename = 'leave_report_{}'.format(datetime.datetime.today().strftime("%Y-%m-%d_%H:%M"))
    return export_logs(data, headers, filename)


def export_logs(data, headers, filename):
    STYLES = dict(
        bold='font: bold 1',
        italic='font: italic 1',

        # Wrap text in the cell
        wrap_bold='font: bold 1; align: wrap 1;',
        wrap='align: wrap 1;',

        # White text on a blue background
        reversed='pattern: pattern solid, fore_color blue; font: color white, bold 1;',

        # Light orange checkered background
        light_orange_bg='pattern: pattern fine_dots, fore_color white, back_color orange;',

        # Heavy borders
        bordered='border: top thick, right thick, bottom thick, left thick;',

        # 16 pt red text
        big_red='font: height 320, color red;',
    )

    wb = Workbook()
    ws = wb.add_sheet("first_sheet")
    ws.fit_num_pages = 1
    ws.fit_height_to_pages = 0
    ws.fit_width_to_pages = 1

    row_index = 0  # header to be written on first row
    for col_index, header in enumerate(headers):
        ws.write(row_index, col_index, header)  # Parameters for ws.write method are "row, column, data item, style"

    row_index = 1  # Data starts on second row
    for row in data:
        for col, value in enumerate(row):
            ws.write(row_index, col, value)
        row_index += 1

    fd, fn = tempfile.mkstemp()
    os.close(fd)
    wb.save(fn)
    fh = open(fn, 'rb')
    resp = fh.read()
    fh.close()
    response = HttpResponse(resp, content_type='application/ms-excel')  # change mimetype to content_type
    response['Content-Disposition'] = 'attachment; filename={}.xls'.format(filename)
    return response



#Displays Admin dashbaord
def admin_view(request):
    context = {}

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    hr = HR.objects.filter(name=name)  # Filters for logged in user in list of HR


    if hr:  # Checks if logged in user is HR
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    elif executive_director:  # Checks if logged in user is the executive director
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    elif director:  # Checks if logged in user is a director
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

    elif line_manager:  # Checks if logged in user is a manager
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




    context['approved_leave'] = approved_leave
    context['pending_leave'] = pending_leave
    context['rejected_leave'] = rejected_leave

    return render(request, 'adminDashboard/index.html', context)

#Displays all approved Leave Requests
def approved(request):
    context = {}

    pending_leave = Leaves.objects.filter(name="")
    approved_leave = Leaves.objects.filter(name="")
    rejected_leave = Leaves.objects.filter(name="")

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    hr = HR.objects.filter(name=name)  # Filters for logged in user in list of HR


    if hr:  # Checks if logged in user is HR
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    elif executive_director:  # Checks if logged in user is the executive director
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    elif director:  # Checks if logged in user is a director
        director = Director.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Pending')
                                                                            | Q(Approval_by_Director='Pending')
                                                                            | Q(Approval_by_Executive_Director='Pending'
                                                                                )).order_by('DateApplied')

        emp_over_thirty_d = exceed_thirty_d(director.DirectorateHeaded, request)
        context['emp_over_thirty'] = emp_over_thirty_d


        approved_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Rejected')
                                                                            | Q(Approval_by_Director='Rejected')
                                                                            | Q(Approval_by_Executive_Director='Rejected'
                                                                                )).order_by('DateApplied')

    elif line_manager:  # Checks if logged in user is a manager
        line_manager = LineManager.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
            | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        emp_over_thirty = exceed_thirty(line_manager.Departments_under, request)
        context['emp_over_thirty'] = emp_over_thirty

        approved_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Rejected') | Q(Approval_by_Director='Rejected')
            | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    context['approved_leave'] = approved_leave
    context['pending_leave'] = pending_leave
    context['rejected_leave'] = rejected_leave

    return render(request, 'adminDashboard/leavemanagement/approvedleaves.html', context)

#Displays all pending Leave Requests
def pending(request):
    context = {}

    pending_leave = Leaves.objects.filter(name="")
    approved_leave = Leaves.objects.filter(name="")
    rejected_leave = Leaves.objects.filter(name="")

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    hr = HR.objects.filter(name=name)  # Filters for logged in user in list of HR


    if hr:  # Checks if logged in user is HR
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    elif executive_director:  # Checks if logged in user is the executive director
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')



    elif director:  # Checks if logged in user is a director
        director = Director.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Pending')
                                                                            | Q(Approval_by_Director='Pending')
                                                                            | Q(Approval_by_Executive_Director='Pending'
                                                                                )).order_by('DateApplied')

        emp_over_thirty_d = exceed_thirty_d(director.DirectorateHeaded, request)
        context['emp_over_thirty'] = emp_over_thirty_d

        approved_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Rejected')
                                                                            | Q(Approval_by_Director='Rejected')
                                                                            | Q(Approval_by_Executive_Director='Rejected'
                                                                                )).order_by('DateApplied')

    elif line_manager:  # Checks if logged in user is a manager
        line_manager = LineManager.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
            | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        emp_over_thirty = exceed_thirty(line_manager.Departments_under, request)
        context['emp_over_thirty'] = emp_over_thirty

        approved_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under,
                                               Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Rejected') | Q(Approval_by_Director='Rejected')
            | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')



    context['approved_leave'] = approved_leave
    context['pending_leave'] = pending_leave
    context['rejected_leave'] = rejected_leave

    return render(request, 'adminDashboard/leavemanagement/pendingleaves.html', context)

#Displays all rejected Leave Requests
def rejected(request):
    context = {}

    pending_leave = Leaves.objects.filter(name="")
    approved_leave = Leaves.objects.filter(name="")
    rejected_leave = Leaves.objects.filter(name="")

    name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

    director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
    line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
    executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
    hr = HR.objects.filter(name=name)  # Filters for logged in user in list of HR


    if hr:  # Checks if logged in user is HR
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    elif executive_director:  # Checks if logged in user is the executive director
        pending_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                                              | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                               | Q(Approval_by_Director='Rejected')
                                               | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    elif director:  # Checks if logged in user is a director
        director = Director.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Pending')
                                                                            | Q(Approval_by_Director='Pending')
                                                                            | Q(Approval_by_Executive_Director='Pending'
                                                                                )).order_by('DateApplied')

        emp_over_thirty_d = exceed_thirty_d(director.DirectorateHeaded, request)
        context['emp_over_thirty'] = emp_over_thirty_d


        approved_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Rejected')
                                                                            | Q(Approval_by_Director='Rejected')
                                                                            | Q(Approval_by_Executive_Director='Rejected'
                                                                                )).order_by('DateApplied')

    elif line_manager:  # Checks if logged in user is a manager
        line_manager = LineManager.objects.get(name=name)
        pending_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
            | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

        emp_over_thirty = exceed_thirty(line_manager.Departments_under, request)
        context['emp_over_thirty'] = emp_over_thirty


        approved_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under, Approval_by_Line_Manager='Approved',
                                               Approval_by_Director='Approved',
                                               Approval_by_Executive_Director='Approved').order_by('DateApplied')

        rejected_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
            Q(Approval_by_Line_Manager='Rejected') | Q(Approval_by_Director='Rejected')
            | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

    context['approved_leave'] = approved_leave
    context['pending_leave'] = pending_leave
    context['rejected_leave'] = rejected_leave

    return render(request, 'adminDashboard/leavemanagement/rejectedleaves.html', context)

#Displays all Leave Requests

class LeaveListView(ListView):
    template_name = "adminDashboard/leavemanagement/allleaves.html"

    def get(self, request, *args, **kwargs):

        context = {}
        all_leave = Leaves.objects.filter(name="")

        name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

        director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
        line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
        executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
        hr = HR.objects.filter(name=name)  # Filters for logged in user in list of HR

        if hr:  # Checks if logged in user is HR
            all_leave = Leaves.objects.all()

            pending_leave = Leaves.objects.filter(
                Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

            approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                                   Approval_by_Executive_Director='Approved').order_by('DateApplied')

            rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                                   | Q(Approval_by_Director='Rejected')
                                                   | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

        elif executive_director:  # Checks if logged in user is a director
            all_leave = Leaves.objects.all()
            pending_leave = Leaves.objects.filter(
                Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

            approved_leave = Leaves.objects.filter(Approval_by_Line_Manager='Approved', Approval_by_Director='Approved',
                                                   Approval_by_Executive_Director='Approved').order_by('DateApplied')

            rejected_leave = Leaves.objects.filter(Q(Approval_by_Line_Manager='Rejected')
                                                   | Q(Approval_by_Director='Rejected')
                                                   | Q(Approval_by_Executive_Director='Rejected'
                                                       )).order_by('DateApplied')

        elif director:  # Checks if logged in user is a director
            director = Director.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded)

            pending_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Pending')
                                                                               | Q(Approval_by_Director='Pending')
                                                                               | Q(Approval_by_Executive_Director='Pending'
                                                                                  )).order_by('DateApplied')

            emp_over_thirty_d = exceed_thirty_d(director.DirectorateHeaded, request)
            context['emp_over_thirty'] = emp_over_thirty_d


            approved_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded, Approval_by_Line_Manager='Approved',
                                                   Approval_by_Director='Approved',
                                                   Approval_by_Executive_Director='Approved').order_by('DateApplied')

            rejected_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded).filter(Q(Approval_by_Line_Manager='Rejected')
                                                                                | Q(Approval_by_Director='Rejected')
                                                                                | Q(Approval_by_Executive_Director='Rejected'
                                                                                    )).order_by('DateApplied')

        elif line_manager:  # Checks if logged in user is a manager
            line_manager = LineManager.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under)

            pending_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
                Q(Approval_by_Line_Manager='Pending') | Q(Approval_by_Director='Pending')
                | Q(Approval_by_Executive_Director='Pending')).order_by('DateApplied')

            emp_over_thirty = exceed_thirty(line_manager.Departments_under, request)
            context['emp_over_thirty'] = emp_over_thirty



            approved_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under,
                                                   Approval_by_Line_Manager='Approved',
                                                   Approval_by_Director='Approved',
                                                   Approval_by_Executive_Director='Approved').order_by('DateApplied')

            rejected_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under).filter(
                Q(Approval_by_Line_Manager='Rejected') | Q(Approval_by_Director='Rejected')
                | Q(Approval_by_Executive_Director='Rejected')).order_by('DateApplied')

        context['all_leave'] = all_leave
        context['approved_leave'] = approved_leave
        context['pending_leave'] = pending_leave
        context['rejected_leave'] = rejected_leave

        return render(request, self.template_name, context)

#Provides extra details of Leave Request
class LeaveDetailView(DetailView):

    template_name = "adminDashboard/leavedetails.html"

    def get(self, request, *args, **kwargs):

        context = {}
        all_leave = Leaves.objects.filter(name="")

        name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

        director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
        line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
        executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
        hr = HR.objects.filter(name=name)  # Filters for logged in user in list of HR

        if hr:  # Checks if logged in user is HR
            all_leave = Leaves.objects.all() #HR needs to be able to see all Leaves but then not have power to aprrove.
                                             #Only HR line manager can approve for their own department but not others.

        elif executive_director:  # Checks if logged in user is executive director
            all_leave = Leaves.objects.all()

        elif director:  # Checks if logged in user is a director
            director = Director.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDirectorate=director.DirectorateHeaded)

        elif line_manager:  # Checks if logged in user is a manager
            line_manager = LineManager.objects.get(name=name)
            all_leave = Leaves.objects.filter(empDepartment=line_manager.Departments_under)

        context['all_leave'] = all_leave
        return render(request, self.template_name, context)

#Handles the approval and rejection of Leave Requests
class LeaveUpdateView(UpdateView):
    template_name = "adminDashboard/status_update.html"

    def get(self, request, *args, **kwargs):
        context = {}

        approval_form = ApprovalForm()

        context['approval_form'] = approval_form

        return render(request, self.template_name, context)

    @staticmethod
    def approved(selected_leave_request, selected_employee, sender):

        hr = HR.objects.all().first()
        name_hr = hr.name
        split_line_name_hr = name_hr.split(' ')
        email_name_hr = Account.objects.get(last_name=split_line_name_hr[1], first_name=split_line_name_hr[0])


        name = selected_employee.name
        split_line_name = name.split(' ')
        email_name = Account.objects.get(last_name=split_line_name[1], first_name=split_line_name[0])


        if selected_leave_request.cancellation_status == True:
            send_mail(
                subject="Leave Request Cancellation",
                message="Hello " + name + " ,\n I have approved the cancellation of this leave request. "
                                          "\n Please go to the NITA Leave Management Portal to action the next phase of this cancellation request.",
                from_email=sender,
                recipient_list=[email_name.email, email_name_hr.email]
            )
            selected_leave_request.OutstandingLeaveDays = selected_leave_request.OutstandingLeaveDays + selected_leave_request.NumberOfDaystaken
            selected_leave_request.save()

        else:
            send_mail(
                subject="Leave Request",
                message="Hello " + name + " ,\n I have approved this leave request. "
                                          "\n Please go to the NITA Leave Management Portal to action the next phase of this request.",
                from_email=sender,
                recipient_list=[email_name.email, email_name_hr.email]
            )



    @staticmethod
    def rejected(selected_employee, sender, reason):
        employee = selected_employee.name
        split_employee = employee.split(' ')
        email_employee = Account.objects.get(last_name=split_employee[1], first_name=split_employee[0])

        if selected_employee.cancellation_status == True:
            send_mail(
                subject="Leave Request",
                message="Hello " + employee + " ,\n Sorry, your cancellation request to take leave has been rejected. The reason is below: \n  " +reason,
                from_email=sender,
                recipient_list=[email_employee.email]
            )
        else:
            send_mail(
                subject="Leave Request",
                message="Hello " + employee + " ,\n Sorry, your request to take leave has been rejected. The reason is below: \n  " + reason,
                from_email=sender,
                recipient_list=[email_employee.email]
            )
            selected_employee.OutstandingLeaveDays = selected_employee.OutstandingLeaveDays + selected_employee.NumberOfDaystaken
            selected_employee.save()

            email_employee.OutstandingLeaveDays = selected_employee.OutstandingLeaveDays
            email_employee.save()

    def post(self, request, *args, **kwargs):

        leave_id = self.kwargs.get('pk')

        selected_leave_request = get_object_or_404(Leaves, pk=leave_id)


        name = request.user.first_name + " " + request.user.last_name  # Name of person currently logged in

        director = Director.objects.filter(name=name)  # Filters for logged in user in list of Directors
        line_manager = LineManager.objects.filter(name=name)  # Filters for logged in user in list of Line Managers
        executive_director = ExecutiveDirector.objects.filter(name=name)  # Filters for logged in user in list of Executive Director
        hr = HR.objects.filter(name=name)  # Filters for logged in user in list of HR

        context = {}
        approval_form = ApprovalForm(request.POST)
        all_leave = Leaves.objects.all()

        context['all_leave'] = all_leave

        if approval_form.is_valid():
            post = approval_form.save(commit=False)
            post.save()

            if executive_director:  # Checks if logged in user is the excutive director
                # Change Executive Director field in leave model to approved
                selected_leave_request.Approval_by_Executive_Director = post.leave_status
                selected_leave_request.save()

                employee = selected_leave_request

                if post.leave_status == "Approved":
                    self.approved(selected_leave_request, employee, request.user.email) #Once ED approves an email is sent to employee that applied for leave

                elif post.leave_status == "Rejected":
                    self.rejected(selected_leave_request, request.user.email, post.notes)

            if director:  # Checks if logged in user is a director
                # Change Director field in leave model to approved
                selected_leave_request.Approval_by_Director = post.leave_status
                selected_leave_request.save()

                # Need to send email to Executive Director to action Leave.
                if post.leave_status == "Approved":
                    obj = Account.objects.get(role="Executive Director") #There should be only one account with the role Executive Director
                    ed_name = obj.first_name + " " + obj.last_name
                    ed = ExecutiveDirector.objects.get(name=ed_name)

                    self.approved(selected_leave_request, ed, request.user.email)

                elif post.leave_status == "Rejected":
                    self.rejected(selected_leave_request, request.user.email, post.notes)

            if line_manager:  # Checks if logged in user is a manager

                # Change Line Manager field in leave model to approved
                selected_leave_request.Approval_by_Line_Manager = post.leave_status
                selected_leave_request.save()
                # Send email to Head of Directorate to action Leave.
                dir = selected_leave_request.empDirector

                if post.leave_status == "Approved":
                    self.approved(selected_leave_request, dir, request.user.email)

                elif post.leave_status == "Rejected":
                    self.rejected(selected_leave_request, request.user.email, post.notes)

            return redirect(reverse("adminDashboard:LeaveDetailView"))



        else:
            context['approval_form'] = approval_form
            return render(request, self.template_name, context)

class MonetaryValueAllStaff(ListView):
    template_name = "adminDashboard/leavemanagement/monetary_value_all_staff.html"

    def get(self, request, *args, **kwargs):

        context = {}

        all_staff = Account.objects.all()

        context['all_staff'] = all_staff

        return render(request, self.template_name, context)


class MonetaryValueSelectedEmployee(ListView):

    template_name = "adminDashboard/leavemanagement/monetary_value_selected_employee.html"

    def get(self, request, *args, **kwargs):
        account_id = self.kwargs.get('pk')
        selected_employee = get_object_or_404(Account, pk=account_id)

        context = {}
        salary_form = SalaryForm()

        print(account_id)
        print(selected_employee.first_name)

        context['selected_employee'] = selected_employee
        context['salary_form'] = salary_form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}

        account_id = self.kwargs.get('pk')
        selected_employee = get_object_or_404(Account, pk=account_id)

        salary_form = SalaryForm(request.POST)

        if salary_form.is_valid():
            salary = salary_form.save(commit=False)

            print("Salary = ")
            print(salary.salary)
            avg_working_days_per_month = 22
            monetary_value_per_day = salary.salary / avg_working_days_per_month
            monetary_value_per_day = round(monetary_value_per_day, 0)

            monetary_value_outstanding_leave_days = monetary_value_per_day * selected_employee.OutstandingLeaveDays
            monetary_value_outstanding_leave_days = round(monetary_value_outstanding_leave_days, 0)

            context['monetary_value_per_day'] = monetary_value_per_day
            context['monetary_value_outstanding_leave_days'] = monetary_value_outstanding_leave_days

        salary_form = SalaryForm()
        context['salary_form'] = salary_form
        context['selected_employee'] = selected_employee

        return render(request, self.template_name, context)


#Display all users to delegate privileges
class Delegate(ListView):
    template_name = "adminDashboard/leavemanagement/delegate.html"

    def get(self, request, *args, **kwargs):

        context = {}

        all_staff = Account.objects.all()

        context['all_staff'] = all_staff

        return render(request, self.template_name, context)


#Assigns privileges to User
def handle(request, slug):

    update_account = get_object_or_404(Account, slug=slug)
    name = update_account.first_name + " " + update_account.last_name

    if request.user.is_line_manager:
        if update_account.is_line_manager == True:
            messages.warning(request, f'This user is already a line manager')
            return redirect('adminDashboard:delegate')

        else:
            update_account.is_line_manager = True
            update_account.is_staff = True
            department = Departments.objects.get(name=request.user.department)
            obj = LineManager(name=name, Departments_under=department)  # Adds User to list of line managers
            obj.save()

    elif request.user.is_director:
        if update_account.is_director == True:
            messages.warning(request, f'This user is already a Director')
            return redirect('adminDashboard:delegate')

        else:
            update_account.is_director = True
            update_account.is_staff = True
            directorate = Directories.objects.get(name=request.user.directorate)
            obj = Director(name=name, DirectorateHeaded=directorate)
            obj.save()

    elif request.user.is_executive_director:
        if update_account.is_executive_director == True:
            messages.warning(request, f'This user is already an Executive Director')
            return redirect('adminDashboard:delegate')

        else:
            update_account.is_executive_director = True
            update_account.is_staff = True
            obj = ExecutiveDirector(name=name)
            obj.save()

    update_account.save()

    return redirect('adminDashboard:pending')

#Removes privileges from User
def remove(request, slug):

    update_account = get_object_or_404(Account, slug=slug)
    name = update_account.first_name + " " + update_account.last_name

    if request.user.is_line_manager:
        if update_account.role == "Line Manager":
            messages.warning(request, f'You cannot change the the privileges of the selected user')
            return redirect('adminDashboard:delegate')

        if update_account.role == "Director" or update_account.role == "Executive Director":
            update_account.is_line_manager = False
            update_account.is_staff = True
            LineManager.objects.filter(name=name).delete()

        else:
            update_account.is_line_manager = False
            update_account.is_staff = False
            LineManager.objects.filter(name=name).delete()

    elif request.user.is_director:
        if update_account.role == "Director":
            messages.warning(request, f'You cannot change the the privileges of the selected user')
            return redirect('adminDashboard:delegate')

        if update_account.role == "Line Manager" or update_account.role == "Executive Director":
            update_account.is_director = False
            update_account.is_staff = True
            Director.objects.filter(name=name).delete()

        else:
            update_account.is_director = False
            update_account.is_staff = False
            Director.objects.filter(name=name).delete()

    elif request.user.is_executive_director:
        if update_account.role == "Executive Director":
            messages.warning(request, f'You cannot change the the privileges of the selected user')
            return redirect('adminDashboard:delegate')

        if update_account.role == "Line Manager" or update_account.role == "Director":
            update_account.is_executive_director = False
            update_account.is_staff = True
            ExecutiveDirector.objects.filter(name=name).delete()

        else:
            update_account.is_executive_director = False
            update_account.is_staff = False
            ExecutiveDirector.objects.filter(name=name).delete()

    update_account.save()

    return redirect('adminDashboard:pending')



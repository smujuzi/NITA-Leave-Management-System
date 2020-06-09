from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render,reverse
from django.http import HttpResponse 
from employeeDashboard.models import Leaves
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


def admin(request):
    status = Leaves.objects.all()

    context = {
        'status': status
    }

    return render(request, 'adminDashboard/index.html', context)


def dashboard(request):
    return render(request, 'adminDashboard/dashboard.html')


def notifications(request):
    return render(request, 'adminDashboard/notifications.html')


def approved(request):
    return render(request, 'adminDashboard/leavemanagement/approvedleaves.html')


def pending(request):
    return render(request, 'adminDashboard/leavemanagement/pendingleaves.html')


def rejected(request):
    return render(request, 'adminDashboard/leavemanagement/rejectedleaves.html')


def history(request):
    return render(request, 'adminDashboard/alleaves.html')


class LeaveListView(ListView):
    model = Leaves
    template_name = "adminDashboard/leavemanagement/allleaves.html"


class LeaveDetailView(DetailView):
    model = Leaves
    template_name = "adminDashboard/leavedetails.html"

class LeaveUpdateView(UpdateView):
    model = Leaves
    fields = ['Approval_by_Line_Manager','Approval_by_Director',
    'Approval_by_Executive_Director']
    pass



#def AllLeaves(request):
#    context = {
#        'all_leaves':LeaveForm.objects.all()
#    }
#    return render(request, 'adminDashboard/leavemanagement/allleaves.html', context)
#def LeaveDetails(request):
#    return render(request, 'adminDashboard/leavedetail.html')











    
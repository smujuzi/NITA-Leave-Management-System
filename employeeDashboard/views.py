from django.shortcuts import render
from adminDashboard.models import *
from employeeDashboard.models import *
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .forms import LeaveForm

#auth_stuff
#from adminDashboard.forms import UserRegistrationForm



#from .forms import AddressForm
from django.urls import reverse_lazy


class ApplyLeaveView(CreateView):
    # return render(request,'leaves_form.html')
    model = Leaves
    form_class = LeaveForm
    template_name = 'leaves_form.html'
    success_url = reverse_lazy('history')
    

@login_required
def leave_history(request):
    leave_history = Leaves.objects.all()
    
    context = {
        'leave_history':leave_history
    }
    return render(request,'history.html', context)




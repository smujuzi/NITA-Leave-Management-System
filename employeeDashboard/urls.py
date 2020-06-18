from django.urls import path
from employeeDashboard import views as employee_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('leavehistory', employee_views.leave_history, name="history"),
    path('', login_required(employee_views.ApplyLeaveView.as_view()), name="apply")
 
]

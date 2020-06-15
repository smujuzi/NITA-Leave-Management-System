from django.urls import path
from employeeDashboard import views as employee_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', employee_views.home, name="home"),
    path('leavehistory', employee_views.leave_history, name="history"),
    path('profile', employee_views.profile, name="profile"),
    path('apply/', login_required(employee_views.ApplyLeaveView.as_view()), name="apply"),

    #authentication_views
    #path('register', views.createuserview.as_view(), name="register")

]
 # path('leaveapply/',views.leave_apply, name="EmpLeaveApply"),
from django.urls import path
from employeeDashboard import views as employee_views


urlpatterns = [
    path('', employee_views.home, name="EmpLogin"),
    path('leavehistory', employee_views.leave_history, name="history"),
    path('profile', employee_views.profile, name="profile"),
    path('apply/', employee_views.ApplyLeaveView.as_view(), name="apply"),

    #authentication_views
    #path('register', views.createuserview.as_view(), name="register")

]
 # path('leaveapply/',views.leave_apply, name="EmpLeaveApply"),
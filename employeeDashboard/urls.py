from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="EmpLogin"),
    path('leavehistory', leave_history, name="history"),
    path('apply/', ApplyLeaveView.as_view(), name="apply"),

    #authentication_views
    path('register', views.createuserview.as_view(), name="register")

]
 # path('leaveapply/',views.leave_apply, name="EmpLeaveApply"),
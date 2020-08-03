
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from employeeDashboard import views as employee_views
from employeeDashboard.views import ApplyLeaveView
from adminDashboard.views import admin_view

app_name = 'employeeDashboard'

urlpatterns = [
    path('leavehistory', employee_views.leave_history, name="history"),
    path('', ApplyLeaveView.as_view(), name="apply"),
    path('adminDashboard', admin_view, name="adminPage"),
 
]

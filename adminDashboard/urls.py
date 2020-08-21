from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from adminDashboard.views import (
    handle,
    remove
)


app_name = 'adminDashboard'
urlpatterns = [
    path('', views.admin_view, name='adminHome'),
    path('delegate/', views.Delegate.as_view(), name="delegate"),
    path('monetary_value_all_staff/', views.MonetaryValueAllStaff.as_view(), name="monetary_value_all_staff"),
    path('monetary_value_selected_employee/<int:pk>/', views.MonetaryValueSelectedEmployee.as_view(), name="monetary_value_selected_employee"),
    path('approved/', views.approved, name="approved"),
    path('pending/', views.pending, name="pending"),
    path('rejected/', views.rejected, name="rejected"),
    path('export_members/', views.export_members_excel, name="export_members"),
    
    # class based views
    path('LeaveListView/', views.LeaveListView.as_view(), name='LeaveListView'),
    path('LeaveDetailView/', views.LeaveDetailView.as_view(), name='LeaveDetailView'),
    path('LeaveUpdateView/<int:pk>/', views.LeaveUpdateView.as_view(), name='LeaveUpdateView'),
    path('handle/<slug>/', handle, name="handle"),
    path('remove/<slug>/', remove, name="remove"),
    
]
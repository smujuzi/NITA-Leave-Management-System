from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings


app_name = 'adminDashboard'
urlpatterns = [
    path('', views.admin_view, name='adminHome'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('notifications/', views.notifications, name="notifications"),
    # path('alleaves/', views.AllLeaves, name="alleaves"),
    path('approved/', views.approved, name="approved"),
    path('pending/', views.pending, name="pending"),
    path('rejected/', views.rejected, name="rejected"),
    path('history/', views.history, name="history"),
    
    # class based views
    path('LeaveListView/', views.LeaveListView.as_view(), name='LeaveListView'),
    path('LeaveDetailView/', views.LeaveDetailView.as_view(), name='LeaveDetailView'),
    path('LeaveUpdateView/<int:pk>/', views.LeaveUpdateView.as_view(), name='LeaveUpdateView'),
    
]
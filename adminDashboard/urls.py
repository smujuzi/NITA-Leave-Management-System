from django.urls import path
from . import views


app_name = 'adminDashboard'
urlpatterns = [
    path('', views.admin, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('notifications/', views.notifications, name="notifications"),
    # path('alleaves/', views.AllLeaves, name="alleaves"),
    path('approved/', views.approved, name="approved"),
    path('pending/', views.pending, name="pending"),
    path('rejected/', views.rejected, name="rejected"),
    path('history/', views.history, name="history"),
    
    # class based views
    path('LeaveListView/', views.LeaveListView.as_view(), name='LeaveListView'),
    path('LeaveDetailView/<int:pk>/', views.LeaveDetailView.as_view(), name='LeaveDetailView'),
    path('LeaveUpdateView/', views.LeaveUpdateView.as_view(), name='LeaveUpdateView')
    
]
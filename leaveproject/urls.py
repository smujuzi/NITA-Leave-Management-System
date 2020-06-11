
from django.contrib import admin
from django.urls import path,include 

urlpatterns = [
    path('employeeDashboard/', include('employeeDashboard.urls')),
    path('adminDashboard/', include('adminDashboard.urls', namespace='adminDashboard')),
    path('', include('UsersAuth.urls')),
    #path('adminsauth/', include('AdminsAuth.urls')),
    path('admin/', admin.site.urls)   
]

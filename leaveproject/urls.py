
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings

from adminDashboard.views import (

        admin_view,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('employeeDashboard/', include('employeeDashboard.urls')),
    path('adminDashboard/', include('adminDashboard.urls', namespace='adminDashboard')),
    path('', include('UsersAuth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

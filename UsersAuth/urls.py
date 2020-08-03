from django.urls import path, include
from UsersAuth import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from UsersAuth.views import (
    login_view,
    RegisterView,

)

urlpatterns = [
    path('', login_view,  name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='usersAuth/logout.html'), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
]
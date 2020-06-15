from django.urls import path 
from UsersAuth import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='usersAuth/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='usersAuth/logout.html'), name="logout"),
    path('register/', user_views.register, name="register")
]
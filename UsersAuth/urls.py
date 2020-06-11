from django.urls import path 
from UsersAuth import views as user_views

urlpatterns = [
    path('', user_views.login, name="login" ),
    path('register/', user_views.register, name="register")
]
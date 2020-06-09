from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def register(UserCreationForm):
    form = UserCreationForm()
    context = {
        'form': form
    }
    return render('UserAuth/register.html', context)
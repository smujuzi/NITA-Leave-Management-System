from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('')
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'UsersAuth/register.html', context)

def login(request):

    context = {

    }
    return render(request, 'UsersAuth/login.html', context)
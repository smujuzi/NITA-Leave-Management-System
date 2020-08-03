from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from UsersAuth.models import Account
from material import Layout, Row, Fieldset
from django.contrib.auth import authenticate

import logging

log = logging.getLogger(__name__)
# convert the errors to text



class CreateUserForm(UserCreationForm): 
    email = forms.EmailField()
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

DEPARTMENT_CHOICES = (
    ("Developers", 'Developers'),
    ("Business Analysts", 'Business Analysts'),
    ("Field", 'Field'),
    ("Deployment", 'Deployment'),
    ("Infrastructure", 'Infrastructure'),
    ("Customer Services", 'Customer Services'),
    ("Policy", 'Policy'),
    ("Contracts", 'Contracts'),
    ("Human Resources", 'Human Resources'),
    ("Procurement", 'Procurement'),
    ("Research", 'Research'),
    ("Planning", 'Planning'),
    ("Director", 'Director'),
)

DIRECTORATE_CHOICES = (
    ("E-government Services", 'E-government Services'),
    ("Technical Services", 'Technical Services'),
    ("Information Security", 'Information Security'),
    ("Regulation and Legal Services", 'Regulation and Legal Services'),
    ("Finance and Administration", 'Finance and Administration'),
    ("Planning, Research and Development", 'Planning, Research and Development'),
    ("Executive Director", 'Executive Director'),
)

STAFF_ROLE_CHOICES = (
    ("Employee", 'Employee'),
    ("Line Manager", 'Line Manager'),
    ("Director", 'Director'),
    ("Executive Director", 'Executive Director'),
)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', help_text='We will communicate to you via email',
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. James'}))
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Lukwago'}))

    department = forms.ChoiceField(label='Department', choices=DEPARTMENT_CHOICES)

    directorate = forms.ChoiceField(label='Directorate', choices=DIRECTORATE_CHOICES)

    role = forms.ChoiceField(label='Role', choices=STAFF_ROLE_CHOICES)


    password1 = forms.CharField(max_length=254, label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter a password'}))
    password2 = forms.CharField(max_length=254, label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'department', 'directorate', 'role', 'email', 'password1', 'password2')

    layout = Layout('first_name', 'last_name', 'department', 'directorate', 'role', 'email', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    password = forms.CharField(max_length=254, label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Enter your password'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

    layout = Layout('email', 'password')





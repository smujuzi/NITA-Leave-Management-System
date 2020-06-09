from django import forms 
from adminDashboard.models import *
from employeeDashboard.models import *


class TimeInput(forms.TimeInput):
    input_type = "time"

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = ['name','DateApplied', 'StartDate',
                'EndDate','OutstandingLeaveDays', 'NumberOfDaystaken',
                'LeaveType','empDirector',
                'empDirectorate', 'empDepartment']
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["DateApplied"].widget = DateInput()
        self.fields["StartDate"].widget = DateInput()
        self.fields["EndDate"].widget = DateInput()




















'''
STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)
class AddressForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(choices=STATES)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=False)

    '''
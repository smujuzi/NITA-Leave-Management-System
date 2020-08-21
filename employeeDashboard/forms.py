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
    OutstandingLeaveDays = forms.IntegerField(widget=forms.TextInput(
        attrs={'readonly': 'readonly', 'placeholder': '26'})) #26 is a random number chosen for placeholder feature to work

    name = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))

    file_upload = forms.FileField(required=False)

    class Meta:
        model = Leaves
        fields = ['name', 'DateApplied', 'StartDate',
                  'EndDate', 'OutstandingLeaveDays', 'NumberOfDaystaken',
                  'LeaveType', 'empDirector',
                  'empDirectorate', 'empDepartment', 'file_upload']

        # added labels for each field above except name and outstandingLeaveDays since they're re-defined on line 27 and 30
        # crispy_forms library expects a 'labels' dictionary mapping each field to its preferred label
        labels = {
            'DateApplied': 'Application Date',
            'StartDate': '1st Day of Leave',
            'EndDate': 'Last Day of Leave',
            'NumberOfDaystaken': 'Number Of Days Taken',
            'LeaveType': 'Type of Leave',
            'empDirector': 'Director',
            'empDirectorate': 'Directorate',
            'empDepartment': 'Department',
            'file_upload': 'Upload File'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["DateApplied"].widget = DateInput()
        self.fields["StartDate"].widget = DateInput()
        self.fields["EndDate"].widget = DateInput()

        # added two labels here because they wont work in the labels dict
        self.fields["name"].label = "Applicant Name"
        self.fields["OutstandingLeaveDays"].label = "Leave Days Remaining"


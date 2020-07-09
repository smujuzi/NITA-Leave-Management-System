from django import forms
from .models import *
from material import Layout, Row, Fieldset

OPTIONS = (
    ("Approved", 'Approved'),
    ("Rejected", 'Rejected'),
    ("Pending", 'Pending'),
)


class ApprovalForm(forms.ModelForm):

    leave_status = forms.CharField(label='Leave Status',
                                   widget=forms.TextInput(
                                       attrs={'placeholder': 'Please type in Approved or Rejected'})
                                   )

    notes = forms.CharField(label='Notes',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Add any comments'}))

    class Meta:
        model = Approve
        fields = ['leave_status', 'notes']

    layout = Layout('leave_status', 'notes')



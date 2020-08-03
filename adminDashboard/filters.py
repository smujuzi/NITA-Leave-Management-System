import django_filters

from adminDashboard.models import *
from employeeDashboard.models import Leaves

class LeaveFilter(django_filters.FilterSet):

    class Meta:
        model = Leaves
        fields = ['name','empDirectorate']

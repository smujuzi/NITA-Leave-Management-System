from django.contrib import admin
from adminDashboard.models import Departments,LineManager,Director,Directories,Approve, ExecutiveDirector


# Register your models here.
admin.site.register(Departments)
admin.site.register(LineManager)
admin.site.register(Director)
admin.site.register(Directories)
admin.site.register(Approve)
admin.site.register(ExecutiveDirector)

from django.db import models
from adminDashboard.models import Approve, Directories,Departments,Director
from django.shortcuts import reverse
# Create your models here.
class Leaves(models.Model):
    class Meta:
        verbose_name = "Leave List"
        verbose_name_plural = "Applied leaves"
    
    LeaveTypeList = (
        ('Annual','Annual'),
        ('Sick','Sick'),
        ('Maternity ','Maternity '),
        ('Paternity','Paternity'),
        ('Compassionate','Compassionate'),
        ('Terminal / Long term illness ','Terminal / Long term illness '),
        ('Study leave with pay ','Study leave with pay '),
        ('Leave without pay ','Leave without pay ')
    )
    #Reference_id = models.CharField(max_length=100, null=True, default='NITA/LMS/001')
    name        = models.CharField(max_length=200, null=True)
    DateApplied = models.DateField(auto_now=False)
    StartDate   = models.DateField(auto_now=False)
    EndDate     = models.DateField(auto_now=False)

    OutstandingLeaveDays = models.IntegerField(null=True, default=30)
    NumberOfDaystaken    = models.IntegerField(null=True)
    LeaveType            = models.CharField(max_length=300, choices=LeaveTypeList, null=True)
    file_upload          = models.FileField(upload_to='documents/files/')
   
    empDirectorate = models.ForeignKey(Directories,on_delete=models.SET_NULL, null=True)
    empDepartment = models.ForeignKey(Departments,on_delete=models.SET_NULL, null=True)
    empDirector = models.ForeignKey(Director,on_delete=models.CASCADE, null=True)

    Approval_by_Line_Manager = models.CharField(max_length=10, default='Pending')
    Approval_by_Director = models.CharField(max_length=10, default='Pending')
    Approval_by_Executive_Director = models.CharField(max_length=10, default='Pending')

    def get_absolute_url(self):
        return reverse("adminDashboard:LeaveDetailView")
    def __str__(self):
        return self.name
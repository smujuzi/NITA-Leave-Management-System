from django.db import models
 
# Create your models here.

class Approve(models.Model):
    status = (
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('Pending','Pending')
    )
    leave_status = models.CharField(choices=status, max_length=20, null=True)
    date_approved = models.DateField(auto_now=True)
    notes = models.TextField(null=True, max_length=35)


class Directories(models.Model):
    name = models.CharField(max_length=200, null=True)
    # DateCreated = models.DateField(auto_now=False)

    def __str__(self):
        return self.name


class Departments(models.Model):
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
    # DepId = models.CharField(primary_key=True,max_length=200)
    directory = models.ForeignKey(Directories, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    short_name = models.CharField(max_length=200, null=True)
    # DateCreated = models.DateField(auto_now=False)

    def __str__(self):
        return self.name 


class Director(models.Model):
    name = models.CharField(max_length=200, null=True)
    DirectorateHeaded = models.ForeignKey(Directories, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name  


class LineManager(models.Model):
    name = models.CharField(max_length=200, null=True)
    Departments_under = models.ForeignKey(Departments,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class ExecutiveDirector(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

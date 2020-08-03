from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
import uuid

# Create your models here.
class userProfile(models.Model):
    pass
    #Department  = models.model(max_length=20, null=True)


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,  department, directorate, role='Employee', is_line_manager=False, is_director=False, is_executive_director=False, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Please tell us your first name')
        if not last_name:
            raise ValueError('Please tell us your first name')
        if not department:
            raise ValueError('Users must provide their department')
        if not directorate:
            raise ValueError('Users must provide their directorate')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            department=department,
            directorate=directorate

        )
        user.role = role
        user.is_line_manager = is_line_manager
        user.is_director = is_director
        user.is_executive_director = is_executive_director
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,  department, directorate, role='', is_line_manager=False, is_director=False, is_executive_director=False, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name.title(),
            last_name=last_name.title(),
            department=department,
            directorate=directorate
        )
        user.role = role
        user.is_line_manager = is_line_manager
        user.is_director = is_director
        user.is_executive_director = is_executive_director
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename):
    file_path = 'account/{name}/{id}-{filename}'.format(
        name=str(instance.full_names).split()[0], id=str(instance.id), filename=filename)
    return file_path


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    department = models.CharField(max_length=1000, null=True, blank=True)
    directorate = models.CharField(max_length=1000, null=True, blank=True)
    role = models.CharField(max_length=200, null=False, blank=False, default='Employee') #There should be only one account with the role Executive Director
    slug = models.SlugField(blank= True, unique=True, default=uuid.uuid4)


    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_line_manager = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    is_executive_director = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department', 'directorate']

    objects = MyAccountManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

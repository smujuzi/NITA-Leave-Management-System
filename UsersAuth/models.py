from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class userProfile(models.Model):
    pass
    #Department  = models.model(max_length=20, null=True)
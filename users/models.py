from django.db import models
from django.contrib.auth.models import AbstractUser
from.manager import UserManager
from django.utils import timezone
# Create your models here.



class User(AbstractUser):
    username= None
    userid=models.CharField(max_length=20, unique=True)
    level=models.CharField(max_length=50, null=True, blank=True)
    department=models.CharField(max_length=50, null=True, blank=True)
    faculty=models.CharField(max_length=50, null=True, blank=True)
    phone=models.IntegerField(null=True,)
    
    
    objects=UserManager( )
    
    USERNAME_FIELD ='userid'
    REQUIRED_FIELDS=[]
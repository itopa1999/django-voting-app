from django.db import models
from users.models import User
# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50, null=True, blank=True)
    matric_no=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField(max_length=50, null=True, blank=True)
    phone=models.IntegerField(null=True,)
    level=models.CharField(max_length=50, null=True, blank=True)
    department=models.CharField(max_length=50, null=True, blank=True)
    faculty=models.CharField(max_length=50, null=True, blank=True)
    voted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

 
class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_vote = models.IntegerField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    nickname= models.CharField(max_length=50, null=True)
    image=models.ImageField(null=True,blank=True)
    manifesto= models.TextField(max_length=350, null=True, blank=True)
    def __str__(self):
        return str(self.student)


class Votes(models.Model):
    position = models.CharField(max_length=80, null=True)
    candidate = models.CharField(max_length=80, null=True)
    voter=models.CharField(max_length=80, null=True,blank=True)
    def __str__(self):
        return str(self.position)
    
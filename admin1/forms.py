from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from users.models import User
from django.forms import ModelForm
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','userid','email' ,'password1', 'password2']
        
        
class UserForm1(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','userid','email','level','department','faculty', 'phone', 'password1', 'password2']
        
        
        
class StudentForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','userid','email','level','department','faculty', 'phone']
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'
        
         
class CandidateForm(forms.ModelForm):
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")
    positionID=forms.ModelChoiceField(queryset=Position.objects.all(),empty_label="Choose Position", to_field_name="id")
    class Meta:
        model = Candidate
        fields = '__all__'
        exclude=['student','position']
        
class VoteForm(forms.ModelForm):
    class Meta:
        model = Votes
        fields ='__all__'
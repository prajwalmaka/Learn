from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentProfile, TeacherProfile

class TeacherRegistrationForm(UserCreationForm):
    qualification = forms.CharField(max_length=100)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'qualification']

class StudentRegistrationForm(UserCreationForm):
    admission_date = forms.DateField()
    parent_email = forms.EmailField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'admission_date', 'parent_email']
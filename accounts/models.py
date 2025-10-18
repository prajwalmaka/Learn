from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TEACHER = 1
    STUDENT = 2
    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    
    def is_teacher(self):
        return self.role == self.TEACHER
    
    def is_student(self):
        return self.role == self.STUDENT

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    admission_date = models.DateField()
    parent_email = models.EmailField(blank=True)
    # Additional student-specific fields

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    # Additional teacher-specific fields
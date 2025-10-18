from django.db import models
from accounts.models import CustomUser

class ClassGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                              limit_choices_to={'role': CustomUser.TEACHER})
    students = models.ManyToManyField(CustomUser, limit_choices_to={'role': CustomUser.STUDENT},
                                    related_name='classes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_student_count(self):
        return self.students.count()
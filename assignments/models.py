from django.db import models
from classes.models import ClassGroup
from accounts.models import CustomUser

class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='homework/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-due_date']

class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                               limit_choices_to={'role': CustomUser.STUDENT})
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    student_notes = models.TextField(blank=True)
    attachment = models.FileField(upload_to='submissions/', blank=True, null=True)
    
    class Meta:
        unique_together = ('homework', 'student')
        ordering = ['-submitted_at']

class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    graded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.submission.student.username} - {self.score}"
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import TeacherRegistrationForm, StudentRegistrationForm
from .models import CustomUser
from .models import TeacherProfile, StudentProfile
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('login')

class TeacherRegisterView(CreateView):
    model = CustomUser
    form_class = TeacherRegistrationForm
    template_name = 'accounts/register_teacher.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = CustomUser.TEACHER
        user.save()
        # Create TeacherProfile with qualification
        qualification = form.cleaned_data.get('qualification')
        TeacherProfile.objects.create(user=user, qualification=qualification)
        return super().form_valid(form)

class StudentRegisterView(CreateView):
    model = CustomUser
    form_class = StudentRegistrationForm
    template_name = 'accounts/register_student.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user.role = CustomUser.STUDENT
            user.save()
            # Create StudentProfile with admission_date and parent_email
            admission_date = form.cleaned_data.get('admission_date')
            parent_email = form.cleaned_data.get('parent_email')
            StudentProfile.objects.create(user=user, admission_date=admission_date, parent_email=parent_email)
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, f"Registration error: {str(e)}")
            return self.form_invalid(form)

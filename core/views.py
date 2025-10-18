from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(TemplateView):
    """Public landing page (visible to all users)"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any public context data here
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    """Authenticated user dashboard (different for teachers/students)"""
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_teacher():
            from classes.models import ClassGroup
            from assignments.models import Homework
            context['classes'] = ClassGroup.objects.filter(
                teacher=self.request.user)[:5]
            context['recent_assignments'] = Homework.objects.filter(
                created_by=self.request.user).order_by('-created_at')[:5]
        else:
            from assignments.models import Homework, Submission
            context['pending_assignments'] = Homework.objects.filter(
                class_group__students=self.request.user
            ).exclude(
                submission__student=self.request.user
            ).order_by('due_date')[:5]
            context['recent_submissions'] = Submission.objects.filter(
                student=self.request.user
            ).order_by('-submitted_at')[:5]
        
        return context
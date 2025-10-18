from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, CreateView, UpdateView, 
                                DetailView, DeleteView, TemplateView)
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
import calendar

from .models import Homework, Submission, Grade
from classes.models import ClassGroup

class HomeworkListView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = 'assignments/homework_list.html'
    
    def get_queryset(self):
        if self.request.user.is_teacher():
            return Homework.objects.filter(created_by=self.request.user)
        return Homework.objects.filter(class_group__students=self.request.user)


class HomeworkCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Homework
    fields = ['title', 'description', 'due_date', 'class_group', 'attachment']
    template_name = 'assignments/homework_form.html'
    success_url = reverse_lazy('homework-list')
    
    def test_func(self):
        return self.request.user.is_teacher()
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_teacher():
            form.fields['class_group'].queryset = ClassGroup.objects.filter(
                teacher=self.request.user)
        return form


class HomeworkDetailView(LoginRequiredMixin, DetailView):
    model = Homework
    template_name = 'assignments/homework_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_student():
            context['submission'] = Submission.objects.filter(
                homework=self.object,
                student=self.request.user
            ).first()
        return context


class SubmissionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Submission
    fields = ['is_completed', 'student_notes', 'attachment']
    template_name = 'assignments/submission_form.html'
    
    def test_func(self):
        return self.request.user == self.get_object().student
    
    def get_success_url(self):
        return reverse('homework-detail', kwargs={'pk': self.object.homework.pk})


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'assignments/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        month = self.request.GET.get('month')
        if month:
            d = datetime.strptime(month, "%Y-%m")
        else:
            d = datetime.today()
        
        cal = calendar.HTMLCalendar()
        html_cal = cal.formatmonth(d.year, d.month)

        if self.request.user.is_teacher():
            assignments = Homework.objects.filter(
                created_by=self.request.user,
                due_date__year=d.year,
                due_date__month=d.month
            )
        else:
            assignments = Homework.objects.filter(
                class_group__students=self.request.user,
                due_date__year=d.year,
                due_date__month=d.month
            )
        
        for assignment in assignments:
            day = assignment.due_date.day
            url = reverse('homework-detail', args=[assignment.id])
            html_cal = html_cal.replace(
                f'>{day}<',
                f'><a href="{url}" class="assignment-day">{day}</a><'
            )

        # Optional: highlight today
        today = datetime.today()
        if today.year == d.year and today.month == d.month:
            html_cal = html_cal.replace(
                f'>{today.day}<',
                f'><span class="today">{today.day}</span><'
            )

        context['calendar'] = mark_safe(html_cal)
        context['month'] = d
        context['prev_month'] = self.get_prev_month(d)
        context['next_month'] = self.get_next_month(d)
        return context

    def get_prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        return prev_month.strftime("%Y-%m")

    def get_next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        return next_month.strftime("%Y-%m")

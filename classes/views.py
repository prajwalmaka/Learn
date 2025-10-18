from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ClassGroup

class ClassListView(LoginRequiredMixin, ListView):
    model = ClassGroup
    template_name = 'classes/class_list.html'
    
    def get_queryset(self):
        if self.request.user.is_teacher():
            return ClassGroup.objects.filter(teacher=self.request.user)
        return self.request.user.classes.all()

class ClassCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClassGroup
    fields = ['name', 'description', 'students']
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('class-list')
    
    def test_func(self):
        return self.request.user.is_teacher()
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

class ClassUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClassGroup
    fields = ['name', 'description', 'students']
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('class-list')
    
    def test_func(self):
        return self.request.user.is_teacher() and self.get_object().teacher == self.request.user

class ClassDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClassGroup
    template_name = 'classes/class_confirm_delete.html'
    success_url = reverse_lazy('class-list')
    
    def test_func(self):
        return self.request.user.is_teacher() and self.get_object().teacher == self.request.user
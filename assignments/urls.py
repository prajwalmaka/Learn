from django.urls import path
from .views import (
    HomeworkListView, HomeworkCreateView,
    HomeworkDetailView, SubmissionUpdateView,
    CalendarView  # Correct import
)

urlpatterns = [
    path('', HomeworkListView.as_view(), name='homework-list'),
    path('create/', HomeworkCreateView.as_view(), name='homework-create'),
    path('<int:pk>/', HomeworkDetailView.as_view(), name='homework-detail'),
    path('<int:pk>/submit/', SubmissionUpdateView.as_view(), name='submission-update'),
    path('calendar/', CalendarView.as_view(), name='calendar-view'),  # Correct path and spelling
]

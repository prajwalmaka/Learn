from django.urls import path
from .views import PerformanceDashboardView, ClassPerformanceView

urlpatterns = [
    path('', PerformanceDashboardView.as_view(), name='performance-dashboard'),
    path('class/<int:pk>/', ClassPerformanceView.as_view(), name='class-performance'),
]
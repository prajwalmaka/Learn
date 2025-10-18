from django.urls import path
from .views import DashboardView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Main landing page
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Authenticated user dashboard
]
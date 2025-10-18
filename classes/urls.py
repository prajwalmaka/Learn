from django.urls import path
from .views import (ClassListView, ClassCreateView, 
                   ClassUpdateView, ClassDeleteView)

urlpatterns = [
    path('', ClassListView.as_view(), name='class-list'),
    path('create/', ClassCreateView.as_view(), name='class-create'),
    path('<int:pk>/update/', ClassUpdateView.as_view(), name='class-update'),
    path('<int:pk>/delete/', ClassDeleteView.as_view(), name='class-delete'),
]
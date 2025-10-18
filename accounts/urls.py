from django.urls import path
from .views import (CustomLoginView, CustomLogoutView, 
                    TeacherRegisterView, StudentRegisterView)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/teacher/', TeacherRegisterView.as_view(), name='register-teacher'),
    path('register/student/', StudentRegisterView.as_view(), name='register-student'),
]
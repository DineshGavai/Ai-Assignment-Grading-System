from django.urls import path
from .views import *

urlpatterns = [
    path("", login, name="login"),
    path('logout/', user_logout, name="logout"),
    path("register/", register, name="register"),
    # Add these later when you create dashboards
    path("student/", student_dashboard, name="student_dashboard"),
    path("teacher/", teacher_dashboard, name="teacher_dashboard"),
    path('create_assignment/', create_assignment, name='create_assignment'),
]
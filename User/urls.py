from django.urls import path
from .views import *

urlpatterns = [
    path("", login, name="login"),
    path('logout/', user_logout, name="logout"),
    path("register/", register, name="register"),
    path("student/", student_dashboard, name="student_dashboard"),
    path("teacher/", teacher_dashboard, name="teacher_dashboard"),
    path('create_assignment/', create_assignment, name='create_assignment'),
    
    # New URLs based on your views file
    path('classroom/<int:classroom_id>/', classroom_detail, name='classroom_detail'),
    path('create_assignment/<int:classroom_id>/', create_assignment, name='create_assignment_for_classroom'),
    path('assignment/<int:assignment_id>/', view_assignment, name='view_assignment'),
    path('submit_assignment/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/', view_submission, name='view_submission'),
    path('add_classroom/', add_classroom, name='add_classroom'),
]
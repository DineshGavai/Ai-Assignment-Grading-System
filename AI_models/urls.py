from django.urls import path
from .views.AGS_views import *
from .views.Mock_interview import *
from .views.resume_builder import *



urlpatterns = [
   #  Assignment Grading System
   path('AGS/',AGS,name="AGS_Model"),
   path('upload/', upload_file, name='upload_file'),

   # Mock Interview models 
   path('Mock_interview/',mock_interview,name="mock_interview"),
   path("Mock_interview/generate_questions/", get_questions, name="generate_questions"),
   path("Mock_interview/evaluate/", evaluate, name="evaluate"),

   # Resume Builder
   path("resume_builder/",resume_builder,name="resume_builder"),
   path("generate_resume/", generate_resume, name="generate_resume"),
]
from django.urls import path
from .views import AGS_views
from .views import Mock_interview
from .views import resume_builder
from .views import test_generator
from .views import chatbot



urlpatterns = [
   #  Assignment Grading System
   path('AGS/',AGS_views.AGS,name="AGS_Model"),
   path('upload/', AGS_views.upload_file, name='upload_file'),

   # Mock Interview models 
   path('Mock_interview/',Mock_interview.mock_interview,name="mock_interview"),
   path("Mock_interview/generate_questions/", Mock_interview.get_questions, name="generate_questions"),
   path("Mock_interview/evaluate/", Mock_interview.evaluate, name="evaluate"),

   # Resume Builder
   path("resume_builder/",resume_builder.resume_builder,name="resume_builder"),
   path("generate_resume/", resume_builder.generate_resume, name="generate_resume"),

   # Test Generator
    path('test-generator/', test_generator.test_generator, name='test_generator'),
    path('start_test/',test_generator.start_test, name='start_test'),
    path('evaluate/', test_generator.evaluate, name='evaluate'),
   
   # Chatbot
   path('chatbot/', chatbot.chatbot, name='chatbot'),
   path('chat/', chatbot.chat, name='chat'),
]
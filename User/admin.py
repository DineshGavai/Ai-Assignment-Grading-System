from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Feedback)
admin.site.register(Classroom)
admin.site.register(Branch)


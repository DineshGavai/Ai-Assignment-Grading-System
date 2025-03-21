# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Classroom

@receiver(post_save, sender=User)
def auto_enroll_student(sender, instance, created, **kwargs):
    # Only process newly created student accounts
    if created and instance.role == 'student' and instance.branch and instance.year_of_study and instance.semester:
        # Find all classrooms matching this student's branch, year, and semester
        matching_classrooms = Classroom.objects.filter(
            subject__branch=instance.branch,
            subject__year_of_study=instance.year_of_study,
            subject__semester=instance.semester
        )
        
        # The enrollment is automatic since we use the get_enrolled_students method
        # No additional records needed as we're using a dynamic query instead of a persistent relationship
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .manager import OwnerManager

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    # Override email field to enforce uniqueness
    username = None
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    college = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)

    # Student-specific fields
    branch = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.CharField(max_length=20, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)

    # Teacher-specific fields
    department = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = OwnerManager()

    def __str__(self):
        return self.username or self.email
    
class Assignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rubric = models.JSONField(blank=True, null=True)  # e.g., {"grammar": 10, "content": 20}
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.teacher.username}"
    
class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('pending', 'Pending'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/%Y/%m/%d/')  # Stores uploaded files
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(blank=True, null=True)  # AI or teacher-assigned score
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
    
class Feedback(models.Model):
    SOURCE_CHOICES = [
        ('ai', 'AI'),
        ('teacher', 'Teacher'),
    ]

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    content = models.TextField()
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='ai')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.submission} ({self.source})"
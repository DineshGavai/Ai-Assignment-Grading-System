import django
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .manager import OwnerManager
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    YEAR_CHOICES = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ]
    
    SEMESTER_CHOICES = [
        (1, '1st Semester'),
        (2, '2nd Semester'),
        (3, '3rd Semester'),
        (4, '4th Semester'),
        (5, '5th Semester'),
        (6, '6th Semester'),
        (7, '7th Semester'),
        (8, '8th Semester'),
    ]

    # Override email field to enforce uniqueness
    username = models.CharField(
    max_length=150, 
    unique=True, 
    null=True, 
    blank=True,
    validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
    error_messages={
        'unique': 'A user with that username already exists .',
    },
)
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    college = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)

    # Student-specific fields
    branch = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES, blank=True, null=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, blank=True, null=True)

    # Teacher-specific fields
    department = models.CharField(max_length=255, blank=True, null=True)
    
    # Rest of the model remains the same
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = OwnerManager()
    
    # Rest of the methods remain the same

class Branch(models.Model):
    name = models.CharField(max_length=50)  # CSE, IT, Mech, EXTC, Civil, AIDS, IoT
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    YEAR_CHOICES = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ]
    
    SEMESTER_CHOICES = [
        (1, '1st Semester'),
        (2, '2nd Semester'),
        (3, '3rd Semester'),
        (4, '4th Semester'),
        (5, '5th Semester'),
        (6, '6th Semester'),
        (7, '7th Semester'),
        (8, '8th Semester'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    branch = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    
    def __str__(self):
        return f"{self.code}: {self.name}"

class Classroom(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    academic_year = models.CharField(max_length=20)  # e.g., "2024-2025"
    
    def __str__(self):
        return f"{self.subject.name} - {self.academic_year}"
    
    def get_enrolled_students(self):
        """Returns all students enrolled in this classroom based on branch/year/semester"""
        return User.objects.filter(
            role='student',
            branch=self.subject.branch,
            year_of_study=self.subject.year_of_study,
            semester=self.subject.semester
        )

class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rubric = models.JSONField(blank=True, null=True)  # e.g., {"grammar": 10, "content": 20}
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.teacher.email}"
    
class Submission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    answer = models.TextField(blank=True)  # For text-based submissions
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded')
    ], default='draft')
    score = models.IntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.first_name}'s submission for {self.assignment.title}"
    
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
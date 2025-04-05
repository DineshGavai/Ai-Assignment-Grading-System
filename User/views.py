from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import User, Classroom, Assignment, Submission, Feedback, Subject , Branch
from django.contrib.auth.decorators import login_required
from .forms import AssignmentForm,SubmissionForm
import json



def register(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        college = request.POST.get("college")
        confirm_password = request.POST.get("confirmPassword")
        role = request.POST.get("role")
        branch = request.POST.get("branch", "")
        year_of_study = request.POST.get("year", "")
        semester = request.POST.get("semester", "")  # Handle empty string
        department = request.POST.get("department", "")

        # Validate required fields
        if not all([full_name, email, mobile, password, confirm_password, role, college]):
            messages.error(request, "All required fields must be filled.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return redirect("register")

        try:
            # Create user with all required fields at once
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name,  # Maps 'name' to first_name
                mobile=mobile,
                college=college,
                role=role,
                branch=branch if role == "student" else None,
                year_of_study=year_of_study if role == "student" else None,
                semester=int(semester) if semester and role == "student" else None,  # Convert to int if provided
                department=department if role == "teacher" else None,
            )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
        except IntegrityError as e:
            messages.error(request, f"Database error: {str(e)}. Please try again.")
            return redirect("register")
        except ValueError as e:
            messages.error(request, f"Invalid data: {str(e)}. Please check your inputs.")
            return redirect("register")
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}. Please try again.")
            return redirect("register")
    branches = list(Branch.objects.values_list('name', flat=True)) 
    context={
        'branches':branches
    }
    return render(request, "register.html",context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        user = User.objects.filter(email=email).first()
        
        user = authenticate(request, email=email, password=password)
        if user:
            if user.role == role:
                auth_login(request, user)
                if role == "student":
                    return redirect("student_dashboard")
                elif role == "teacher":
                    return redirect("teacher_dashboard")
            else:
                messages.error(request, "Role does not match.")
        else:
            messages.error(request, "Invalid email or password.")
        return redirect("login")
    
    return render(request, "login.html")


@login_required(login_url="login")
def student_dashboard(request):
    # Get all classrooms for this student based on branch, year, and semester
    classrooms = Classroom.objects.filter(
        subject__branch=request.user.branch,
        subject__year_of_study=request.user.year_of_study,
        subject__semester=request.user.semester
    )
    
    # Get all assignments from these classrooms
    assignments = Assignment.objects.filter(classroom__in=classrooms)
    
    # Get student's submissions
    submissions = Submission.objects.filter(student=request.user)
    
    context = {
        'classrooms': classrooms,
        'assignments': assignments,
        'submissions': submissions
    }
    
    return render(request, "student_dashboard.html", context)


@login_required(login_url="login")
def teacher_dashboard(request):
    # Get all classrooms where this teacher is the instructor
    classrooms = Classroom.objects.filter(teacher=request.user)
    
    # Get all assignments created by this teacher
    assignments = Assignment.objects.filter(teacher=request.user)
    
    # Get recent submissions for assignments in teacher's classrooms
    recent_submissions = Submission.objects.filter(
        assignment__classroom__in=classrooms
    ).order_by('-submitted_at')[:10]
    
    context = {
        'classrooms': classrooms,
        'assignments': assignments,
        'recent_submissions': recent_submissions
    }
    
    return render(request, "teacher_dashboard.html", context)


@login_required(login_url="login")
def classroom_detail(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    
    # Security check: ensure the user should have access to this classroom
    if request.user.role == 'teacher' and classroom.teacher != request.user:
        messages.error(request, "You don't have permission to access this classroom.")
        return redirect('teacher_dashboard')
    
    if request.user.role == 'student':
        # Check if student belongs to this classroom's branch/year/semester
        if (request.user.branch != classroom.subject.branch or 
            request.user.year_of_study != classroom.subject.year_of_study or 
            request.user.semester != classroom.subject.semester):
            messages.error(request, "You don't have permission to access this classroom.")
            return redirect('student_dashboard')
    
    # Get all assignments for this classroom
    assignments = Assignment.objects.filter(classroom=classroom)
    
    context = {
        'classroom': classroom,
        'assignments': assignments,
    }
    
    # If teacher, include list of enrolled students
    if request.user.role == 'teacher':
        enrolled_students = User.objects.filter(
            role='student',
            branch=classroom.subject.branch,
            year_of_study=classroom.subject.year_of_study,
            semester=classroom.subject.semester
        )
        context['enrolled_students'] = enrolled_students
    
    return render(request, 'classroom_detail.html', context)


@login_required(login_url="login")
def create_assignment(request, classroom_id=None):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can create assignments.")
        return redirect('teacher_dashboard')
    
    # If classroom_id is provided, pre-select that classroom
    classroom = None
    if classroom_id:
        classroom = get_object_or_404(Classroom, id=classroom_id)
        # Security check: only the teacher of this classroom can create assignments
        if classroom.teacher != request.user:
            messages.error(request, "You can only create assignments for your own classrooms.")
            return redirect('teacher_dashboard')

    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            
            # If classroom_id was provided, use that classroom
            if classroom_id:
                assignment.classroom = classroom
            
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('classroom_detail', classroom_id=assignment.classroom.id)
    else:
        # If classroom was provided, pre-select it in the form
        initial_data = {}
        if classroom:
            initial_data = {'classroom': classroom}
        form = AssignmentForm(initial=initial_data)
        
        # Filter form's classroom choices to only show this teacher's classrooms
        form.fields['classroom'].queryset = Classroom.objects.filter(teacher=request.user)

    return render(request, 'create_assignment.html', {'form': form})


@login_required(login_url="login")
def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    classroom = assignment.classroom
    
    # Security check
    if request.user.role == 'teacher' and assignment.teacher != request.user:
        messages.error(request, "You don't have permission to view this assignment.")
        return redirect('teacher_dashboard')
    
    if request.user.role == 'student':
        # Check if student belongs to this classroom's branch/year/semester
        if (request.user.branch != classroom.subject.branch or 
            request.user.year_of_study != classroom.subject.year_of_study or 
            request.user.semester != classroom.subject.semester):
            messages.error(request, "You don't have permission to view this assignment.")
            return redirect('student_dashboard')
    
    # Check if student has already submitted this assignment
    submission = None
    if request.user.role == 'student':
        submission = Submission.objects.filter(
            student=request.user,
            assignment=assignment
        ).first()
    
    # For teachers, get all submissions for this assignment
    submissions = []
    if request.user.role == 'teacher':
        submissions = Submission.objects.filter(assignment=assignment)
    
    context = {
        'assignment': assignment,
        'submission': submission,
        'submissions': submissions
    }
    
    return render(request, 'view_assignment.html', context)


@login_required(login_url="login")
def submit_assignment(request, assignment_id):
    if request.user.role != 'student':
        messages.error(request, "Only students can submit assignments.")
        return redirect('teacher_dashboard')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    classroom = assignment.classroom
    
    # Check if student belongs to this classroom's branch/year/semester
    if (request.user.branch != classroom.subject.branch or 
        request.user.year_of_study != classroom.subject.year_of_study or 
        request.user.semester != classroom.subject.semester):
        messages.error(request, "You don't have permission to submit to this assignment.")
        return redirect('student_dashboard')
    
    # Check if student has already submitted
    existing_submission = Submission.objects.filter(
        student=request.user,
        assignment=assignment
    ).first()
    
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES, instance=existing_submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.status = 'submitted'  # Reset status if resubmitting
            submission.save()
            
            # TODO: Trigger AI grading here or queue for background processing
            
            messages.success(request, "Assignment submitted successfully!")
            return redirect('view_assignment', assignment_id=assignment_id)
    else:
        form = SubmissionForm(instance=existing_submission)
    
    context = {
        'form': form,
        'assignment': assignment,
        'is_resubmission': existing_submission is not None
    }
    
    return render(request, 'submit_assignment.html', context)


@login_required(login_url="login")
def view_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    assignment = submission.assignment
    
    # Security check
    if request.user.role == 'teacher' and assignment.teacher != request.user:
        messages.error(request, "You don't have permission to view this submission.")
        return redirect('teacher_dashboard')
    
    if request.user.role == 'student' and submission.student != request.user:
        messages.error(request, "You don't have permission to view this submission.")
        return redirect('student_dashboard')
    
    # Get feedback for this submission
    feedback = Feedback.objects.filter(submission=submission).order_by('created_at')
    
    context = {
        'submission': submission,
        'assignment': assignment,
        'feedback': feedback
    }
    
    return render(request, 'view_submission.html', context)


@login_required(login_url="login")
def add_classroom(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can create classrooms.")
        return redirect('teacher_dashboard')
    
    if request.method == "POST":
        # Extract form data
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        academic_year = request.POST.get('academic_year')
        
        if not all([name, subject_id, academic_year]):
            messages.error(request, "All fields are required.")
            return redirect('add_classroom')
        
        try:
            subject = Subject.objects.get(id=subject_id)
            
            # Create the classroom
            classroom = Classroom.objects.create(
                name=name,
                subject=subject,
                teacher=request.user,
                academic_year=academic_year
            )
            
            messages.success(request, f"Classroom '{name}' created successfully!")
            return redirect('classroom_detail', classroom_id=classroom.id)
            
        except Subject.DoesNotExist:
            messages.error(request, "Selected subject does not exist.")
            return redirect('add_classroom')
        except Exception as e:
            messages.error(request, f"Error creating classroom: {str(e)}")
            return redirect('add_classroom')
    
    # Get subjects appropriate for this teacher's department
    subjects = Subject.objects.all()
    if request.user.department:
        subjects = subjects.filter(branch=request.user.department)
    
    context = {
        'subjects': subjects
    }
    
    return render(request, 'add_classroom.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


# AI Feedback generation (this would be triggered after submission)
def generate_ai_feedback(submission_id):
    """
    This function would be called by a background task after submission
    or could be triggered manually by the teacher
    """
    try:
        submission = Submission.objects.get(id=submission_id)
        
        # TODO: Implement AI grading logic here
        # For now, we'll just create a placeholder feedback
        
        feedback_content = "This is automated AI feedback. The submission has been reviewed."
        score = 70  # Sample score
        
        # Create the feedback
        feedback = Feedback.objects.create(
            submission=submission,
            content=feedback_content,
            source='ai'
        )
        
        # Update submission status and score
        submission.status = 'graded'
        submission.score = score
        submission.save()
        
        return True
    except Exception as e:
        print(f"Error generating AI feedback: {str(e)}")
        return False
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login ,logout
from .models import User  
from django.contrib.auth.decorators import login_required
from .forms import AssignmentForm


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

    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        user = User.objects.filter(email=email).first()
        
        user = authenticate(request, email=email, password=password)
        print(user)
        if user:
            if user.role == role:
                auth_login(request, user)
                if role == "student":
                    return redirect("student_dashboard")  # Define this URL later
                elif role == "teacher":
                    return redirect("teacher_dashboard")  # Define this URL later
            else:
                messages.error(request, "Role does not match.")
        else:
            messages.error(request, "Invalid email or password.")
        return redirect("login")
    
    return render(request, "login.html")
@login_required(login_url="login")
def student_dashboard(request):
    return render(request,"student_dashboard.html")
@login_required(login_url="login")
def teacher_dashboard(request):
    return render(request,"teacher_dashboard.html")


@login_required(login_url="login")
def create_assignment(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can create assignments.")
        return redirect('home')  # Adjust to your home URL

    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user  # Set the logged-in teacher
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('teacher_dashboard')  # Adjust to your dashboard URL
    else:
        form = AssignmentForm()

    return render(request, 'create_assignment.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')
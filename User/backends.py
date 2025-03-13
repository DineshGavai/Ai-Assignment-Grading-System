# your_app/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username  # Django uses "username" even if it's actually an email
        print(f"Backend: Attempting to authenticate - Email: {email}, Password: {password}")
        
        try:
            user = User.objects.get(email=email)
            print(f"Backend: User found - Username: {user.username}, Email: {user.email}, Password Hash: {user.password}")
            
            if user.check_password(password):
                print(f"Backend: Password matches - Returning user: {user}")
                return user
            else:
                print("Backend: Password does not match")
                return None
        except User.DoesNotExist:
            print("Backend: No user found with this email")
            return None

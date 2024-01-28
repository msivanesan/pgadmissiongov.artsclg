# backends.py
from django.contrib.auth.backends import BaseBackend
from .models import CustomUserStudent

class CustomUserStudentAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUserStudent.objects.get(username=username)
            if user.check_password(password):
                return user
        except CustomUserStudent.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUserStudent.objects.get(pk=user_id)
        except CustomUserStudent.DoesNotExist:
            return None

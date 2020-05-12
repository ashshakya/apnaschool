from django.contrib.auth.backends import ModelBackend

from apnaschool.accounts.models import Student


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, username=None):
        try:
            return Student.objects.get(username=username)
        except Student.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None

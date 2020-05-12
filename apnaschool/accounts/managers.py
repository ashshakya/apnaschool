import binascii
import os

from django.contrib.auth.models import BaseUserManager

from apnaschool.utils import timezone


def _generate_code():
    return binascii.hexlify(os.urandom(20))


class UserManager(BaseUserManager):

    @classmethod
    def normalizeemail(cls, email):
        """
        Normalize the email address by lowercasing all of it.
        """
        email = email or ''
        email = email.lower()
        return email

    def _create_user(self, email, mobile, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now_local()

        if not email and not mobile:
            raise ValueError('Email/mobile must be set for the user')

        email = self.normalizeemail(email) if email else None
        user = self.model(
            email=email, mobile=mobile, last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self, email=None, mobile=None, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, mobile, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, None, password, **extra_fields)

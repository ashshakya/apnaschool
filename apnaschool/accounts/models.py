from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, Group, Permission, PermissionsMixin
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from apnaschool.accounts.managers import UserManager
# from apnaschool.authtools.models import AbstractNamedUser
from apnaschool.utils import try_or, timezone
from apnaschool.utils.models import TimeStampModel
from apnaschool.data.models import (
    Address, Department, Standard, FeeStructure, StudentsCategory
)


class GenderType:
    MALE = 1
    FEMALE = 2


class UserTypes:
    STAFF = 1
    EMPLOYEE = 2
    STUDENT = 3


class Category:
    GENERAL = 1
    SPECIAL = 2


class UserAbstract(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    GENDER_CHOICES = (
        (None, 'Please select the gender.'),
        (GenderType.MALE, 'Male'),
        (GenderType.FEMALE, 'Female')
    )

    first_name = models.CharField(
        max_length=128, blank=True, null=True, default=''
    )
    middle_name = models.CharField(
        max_length=128, blank=True, null=True, default=''
    )
    last_name = models.CharField(
        max_length=128, blank=True, null=True, default=''
    )
    email = models.EmailField(
        max_length=256, blank=True, null=True, db_column='email',
        unique=True, db_index=True
    )
    is_active = models.BooleanField(default=False)

    unique_code = models.CharField(
        max_length=64, unique=True, blank=True,
        null=True, editable=False, db_index=True
    )
    mobile = models.CharField(
        max_length=13, blank=True, null=True, db_index=True
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, null=True, blank=True
    )
    dob = models.DateField(null=True, blank=True)

    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    class Meta:
        abstract = True

    def __str__(self):
        """
            Returns the email of the User when it is printed in the console
        """
        return f'{self.email} - {self.unique_code}'

    def get_full_name(self):
        """
            Returns the full name of the user.
        """
        full_name = self.first_name
        if self.middle_name:
            full_name = f'{full_name} {self.middle_name}'
        if self.last_name:
            full_name = f'{full_name} {self.last_name}'
        return try_or(lambda: full_name.title(), '')

    def create_unique_code(self, prefix='EM'):
        """
            Create a unique code for the user.
            Defaults to DI.
        """
        return f'{prefix}{str(self.pk).zfill(10 - len(prefix))}'


class Employee(UserAbstract):

    USER_TYPE_CHOICES = (
        (None, 'Please select a user type.'),
        (UserTypes.STAFF, 'Staff'),
        (UserTypes.EMPLOYEE, 'Employee'),
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, blank=True, null=True
    )
    primary_address = models.OneToOneField(
        Address, null=True, blank=True, default=None,
        related_name='employee_primary_address', on_delete=models.DO_NOTHING
    )
    secondary_address = models.OneToOneField(
        Address, null=True, blank=True, default=None,
        related_name='employee_secondary_address', on_delete=models.DO_NOTHING
    )
    department = models.ForeignKey(
        Department, null=True, blank=True,
        default=None, on_delete=models.DO_NOTHING,
        related_name='department'
    )
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='employee_set',
        related_query_name='employee',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='employee_set',
        related_query_name='employee',
    )
    objects = UserManager()

    # Email address to be used as the username
    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name_plural = 'Employees'

    def save(self, *args, **kwargs):
        # We have to save the user object once because, it hasn't been assigned
        # a `pk` yet.
        self.is_active = True
        super().save(*args, **kwargs)  # Call the 'real' save() method.
        if self.unique_code:
            if 'ST' in self.unique_code and self.user_type == UserTypes.EMPLOYEE:
                raise ValidationError(
                    'Student cannot be set as Employee.'
                )
            elif 'EM' in self.unique_code and self.user_type == UserTypes.STUDENT:
                raise ValidationError(
                    'Employee connot be set as Student.'
                )
        else:
            self.unique_code = self.create_unique_code(prefix='EM')
        super().save()


class Student(UserAbstract):

    category = models.ForeignKey(
        StudentsCategory, default=None, blank=True, null=True,
        on_delete=models.CASCADE
    )
    primary_address = models.OneToOneField(
        Address, null=True, blank=True, default=None,
        related_name='student_primary_address', on_delete=models.DO_NOTHING
    )
    secondary_address = models.OneToOneField(
        Address, null=True, blank=True, default=None,
        related_name='student_secondary_address', on_delete=models.DO_NOTHING
    )
    standard = models.ForeignKey(
        Standard, null=True, blank=True,
        default=None, on_delete=models.DO_NOTHING,
        related_name='standard'
    )

    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     help_text=_(
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ),
    #     related_name='student_set',
    #     related_query_name='student',
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     help_text=_('Specific permissions for this user.'),
    #     related_name='student_set',
    #     related_query_name='student',
    # )

    # Email address to be used as the username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name_plural = 'Students'

    def save(self, *args, **kwargs):
        # We have to save the user object once because, it hasn't been assigned
        # a `pk` yet.
        self.set_unusable_password()
        super().save(*args, **kwargs)  # Call the 'real' save() method.
        # if self.unique_code:
        #     if 'ST' in self.unique_code and self.user_type == UserTypes.EMPLOYEE:
        #         raise ValidationError(
        #             'Student cannot be set as Employee.'
        #         )
        #     elif 'EM' in self.unique_code and self.user_type == UserTypes.STUDENT:
        #         raise ValidationError(
        #             'Employee connot be set as Student.'
        #         )
        # else:
        if not self.unique_code:
            self.unique_code = self.create_unique_code(prefix='ST')
        super().save()

    @property
    def is_fee_paid(self):
        from apnaschool.ops.models import Transactions
        txn = Transactions.objects.filter(
            student=self,
            created_at__month=timezone.now_local(only_date=True).month
        )
        return True if txn.exists() else False

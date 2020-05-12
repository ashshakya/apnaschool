# from apnaschool.authtools.admin import NamedUserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjUserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q
from django.utils.crypto import get_random_string
from simple_history.admin import SimpleHistoryAdmin

from apnaschool.accounts.models import Student
from apnaschool.ops.models import Transactions
from apnaschool.utils import (
    InputFilter, DropdownFilter, RelatedDropdownFilter,
    timezone
)
from apnaschool.accounts.forms import CustomUserCreationForm

# from apnaschool.authtools.admin import NamedUserAdmin


class EmailFilter(InputFilter):
    parameter_name = 'email'
    title = 'Email'

    def queryset(self, request, queryset):
        if self.value() is not None:
            email = self.value()

            return queryset.filter(
                Q(email=email)
            )


class MobileFilter(InputFilter):
    parameter_name = 'mobile'
    title = 'Mobile'

    def queryset(self, request, queryset):
        if self.value() is not None:
            mobile = self.value()

            return queryset.filter(
                Q(mobile=mobile)
            )


class ChangedDataSimpleHistoryAdmin(SimpleHistoryAdmin):
    """
    Custom history settings for displaying changed fields and changed values
    """
    history_list_display = ['changed_fields', 'changed_values']

    def changed_fields(self, obj):
        """
        Function for getting the changed fields
        """
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def changed_values(self, obj):
        """
        Function for getting the changed values with respective fields
        """
        changed_fields = self.changed_fields(obj) or []
        changed_values = {}
        for fields in changed_fields:
            changed_values.update({
                fields: [
                    obj.__getattribute__(fields),
                    obj.prev_record.__getattribute__(fields)
                ]
            })
        return changed_values


class UserAdminAbstract(DjUserAdmin, ChangedDataSimpleHistoryAdmin):
    add_form = CustomUserCreationForm

    date_hierarchy = 'created_at'
    list_display = ('email', 'first_name', 'last_name', 'unique_code',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('id', 'first_name', 'last_name', 'email',
                     'unique_code', 'mobile',)
    # filter_horizontal = ('groups', 'user_permissions',)

    readonly_fields = (
        'created_at', 'unique_code'
    )
    ordering = ('-created_at',)


@admin.register(get_user_model())
class EmployeeAdmin(UserAdminAbstract):

    list_filter = (
        EmailFilter, MobileFilter, 'user_type', 'is_active', 'is_superuser',
        'department',
    )
    list_display = (
        'email', 'first_name', 'last_name', 'unique_code', 'department',
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                ('first_name', 'middle_name', 'last_name'),
            )
        }),
        ('Basic Details', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('unique_code', 'gender', 'dob', 'mobile', 'user_type')
        }),
        ('Roles/Permissions', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                ('department', 'is_active', 'is_staff', 'is_superuser')
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at')
        }),
        ('Addresses', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                'primary_address', 'secondary_address',
            )
        }),
    )


class IsFeePaidFilter(admin.SimpleListFilter):
    title = 'is_fee_paid'
    parameter_name = 'is_fee_paid'

    def lookups(self, request, model_admin):
        return (
            (True, True),
            (False, False),
        )

    def queryset(self, request, queryset):
        # import ipdb;ipdb.set_trace()
        value = self.value()
        # if value:
        #     return self.is_fee_paid(value)
        # elif value is False:
        if value in ['True', 'False']:
            return self.is_fee_paid(value)
        return queryset

    def is_fee_paid(self, value):
        transaction = Transactions.objects.filter(
            created_at__month=timezone.now_local(only_date=True).month
        )
        if value == 'True':
            students = Student.objects.filter(
                id__in=transaction.values_list('student__id')
            )
        else:
            students = Student.objects.filter(
                ~Q(
                    id__in=transaction.values_list('student__id')
                )
            )
        return students


@admin.register(Student)
class StudentAdmin(UserAdminAbstract):
    list_filter = (
        EmailFilter, IsFeePaidFilter,
        ('standard', RelatedDropdownFilter),
    )
    # date_hierarchy = 'current_month_fee_paid'
    list_display = (
        'email', 'first_name', 'last_name', 'unique_code',
        'standard', 'category', 'current_month_fee_paid', 'pay_fee'
    )

    # add_fieldsets = (
    #     (None, {
    #         'description': (
    #             'Enter the new user\'s name and email address and click save.'
    #         ),
    #         'fields': ('email', 'first_name', 'last_name',),
    #     }),
    # )

    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address."
            ),
            'fields': ('email', 'first_name',),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                ('first_name', 'middle_name', 'last_name'),
            )
        }),
        ('Basic Details', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('unique_code', 'gender', 'dob', 'mobile')
        }),
        ('Roles/Permissions', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                ('standard', 'category', 'is_active')
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at')
        }),
        ('Addresses', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                'primary_address', 'secondary_address',
            )
        }),
    )

    def current_month_fee_paid(self, obj):
        txn = Transactions.objects.filter(
            student=obj,
            created_at__month=timezone.now_local(only_date=True).month
        )

        return True if txn.exists() else False
    current_month_fee_paid.boolean = True

    def pay_fee(self, obj):
        from django.utils.html import format_html
        url = 'http://128.199.34.252/'
        return format_html('<a href="{}" target="_blank">Pay Fee</a>', url)
    pay_fee.allow_tags = True
    pay_fee.short_description = 'Pay Fee'

from django.contrib import admin
from django.db.models import Q
from django.urls import path

from apnaschool.ops.models import Transactions, PayFee
from apnaschool.utils import InputFilter
from apnaschool.ops.views import TransactionView


class UniqueCodeFilter(InputFilter):
    parameter_name = 'unique_code'
    title = 'Unique Code'

    def queryset(self, request, queryset):
        if self.value() is not None:
            unique_code = self.value()

            return queryset.filter(
                Q(student__unique_code=unique_code)
            )


class ReceiptNumberFilter(InputFilter):
    parameter_name = 'receipt_no'
    title = 'Receipt Number'

    def queryset(self, request, queryset):
        if self.value() is not None:
            receipt_no = self.value()

            return queryset.filter(
                Q(receipt_no=receipt_no)
            )


@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):

    list_filter = (
        UniqueCodeFilter, ReceiptNumberFilter, 'student__standard',
    )
    list_display = (
        'student_full_name', 'student_unique_code',
        'class_name', 'receipt_no', 'created_at',
    )

    readonly_fields = (
        'receipt_no',
    )
    raw_id_fields = ('student', 'tution_fee',)

    def student_full_name(self, obj):
        return obj.student.get_full_name()

    def student_unique_code(self, obj):
        return obj.student.unique_code

    def class_name(self, obj):
        return obj.tution_fee.standard


@admin.register(PayFee)
class PayFeeAdmin(admin.ModelAdmin):
    model = PayFee

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('', TransactionView.as_view(), name=view_name),
        ]

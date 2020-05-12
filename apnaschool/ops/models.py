from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from apnaschool.utils import try_or, timezone
from apnaschool.utils.models import TimeStampModel
from apnaschool.accounts.models import Student
from apnaschool.data.models import Address, Department, Standard, FeeStructure


class Transactions(TimeStampModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name='transaction_set'
    )
    receipt_no = models.CharField(max_length=50, blank=True, null=True)
    tution_fee = models.ForeignKey(
        FeeStructure, on_delete=models.DO_NOTHING
    )
    pending_balance = models.FloatField(
        validators=[MinValueValidator(0.0)], blank=True, null=True
    )
    concession = models.FloatField(
        validators=[MinValueValidator(0.0)],
        blank=True, null=True
    )
    other_charges = models.FloatField(
        validators=[MinValueValidator(0.0)], blank=True, null=True
    )
    remarks = models.CharField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return '{}'.format(self.student.get_full_name())

    def save(self, *args, **kwargs):
        standard = self.student.standard
        self.tution_fee = FeeStructure.objects.get(
            standard=standard
        )
        self.concession = (
            (self.student.category.discount_on_fee / 100) * self.tution_fee.fee
        )
        self.check_max_concession()
        super().save(*args, **kwargs)  # Call the 'real' save() method.
        self.receipt_no = self.generate_receipt_number(prefix='T')
        super().save()

    def generate_receipt_number(self, prefix='T'):
        """
        Format: "TST-YYYYMMDD-pk"
        """

        prefix += str(self.student.unique_code[:2])
        created_at = self.created_at.strftime("%Y%m%d")
        return f'{prefix}-{created_at}-{str(self.pk)}'

    def check_max_concession(self):
        if self.concession > self.tution_fee.fee:
            raise ValidationError(
                'concession cannot be greater than tution fee.'
            )


class PayFee(TimeStampModel):

    class Meta:
        verbose_name_plural = 'Pay Fee'
        app_label = 'ops'

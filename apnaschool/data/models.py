from django.conf import settings
from django.db import models

from apnaschool.utils import timezone
from apnaschool.utils.models import TimeStampModel


def document_upload(instance, filename):
    """
    Stores the attachment in a 'per private-documents/module-type/yyyy/mm/dd' folder.
    :param instance, filename
    :returns ex: private-documents/personalimage/2020/03/10/filename
    """
    today = timezone.get_today_start()
    return 'private-documents/{model}-{type}/{year}/{month}/{day}/{filename}'.format(
        model=instance._meta.model_name,
        type=instance.get_type_display().replace(' ', ''),
        year=today.year, month=today.month,
        day=today.day, filename=filename,
    )


def file_upload(instance, filename):
    """
    Stores the attachment in a 'per private-documents/module-type/yyyy/mm/dd' folder.
    :param instance, filename
    :returns ex: private-documents/personalimage/2020/03/10/filename
    """
    today = timezone.get_today_start()
    return 'transaction-documents/{model}/{year}/{month}/{day}/{filename}'.format(
        model=instance._meta.model_name, year=today.year, month=today.month,
        day=today.day, filename=filename,
    )


def upload_image(instance, image):
    """
    Stores the attachment in a 'per ams-gallery/module-type/yyyy/mm/dd' folder.
    :param instance, filename
    :returns ex: apnaschool-gallery/User-profile/2016/03/30/filename
    """
    today = timezone.get_today_start()
    return 'apnaschool-gallery/{model}/{year}/{month}/{day}/{pk}_{image}'.format(
        model=instance._meta.model_name,
        year=today.year, month=today.month,
        day=today.day, pk=instance.pk, image=image,
    )


class State(TimeStampModel):
    state_name = models.CharField(max_length=128, blank=True, null=True)
    gst_code = models.CharField(max_length=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.state_name}'


class City(TimeStampModel):
    city_name = models.CharField(max_length=128, blank=True, null=True)
    state = models.ForeignKey(
        State, blank=True, null=True, default=None,
        on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f'{self.city_name}'


class Address(TimeStampModel):
    address_line1 = models.CharField(max_length=128, blank=True, null=True)
    address_line2 = models.CharField(max_length=128, blank=True, null=True)
    address_line3 = models.CharField(max_length=128, blank=True, null=True)
    city = models.ForeignKey(
        City, blank=True, null=True, default=None, on_delete=models.PROTECT
    )
    pincode = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def get_full_address(self):
        address = self.address_line1
        if self.address_line2:
            address = '{} {}'.format(address, self.address_line2)
            if self.address_line3:
                address = '{} {}'.format(address, self.address_line3)
        return address


class Department(TimeStampModel):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(
        max_length=128, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f'{self.name}-{self.code}'


class Standard(TimeStampModel):
    class_name = models.CharField(max_length=50, blank=True, null=True)
    class_number = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Standards'

    def __str__(self):
        return f'{self.class_name}-{self.class_number}'


class StudentsCategory(TimeStampModel):
    category_name = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, unique=True)
    discount_on_fee = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = 'Student Category'

    def __str__(self):
        return f'{self.category}'


class FeeStructure(TimeStampModel):
    standard = models.OneToOneField(
        Standard, on_delete=models.CASCADE
    )
    fee = models.FloatField()

    def __str__(self):
        return f'{self.standard.class_name} has Fee Rs.{self.fee}'

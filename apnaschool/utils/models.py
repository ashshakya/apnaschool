from django.db import models


class TimeStampModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Manually append `modified_at` to the field list if `update_fields`
        # argument is sent while saving the instance.
        if kwargs.get('update_fields'):
            kwargs.update({
                'update_fields': kwargs.get('update_fields').append('modified_at')
            })
        return super().save(*args, **kwargs)

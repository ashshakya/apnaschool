from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError


def file_extension_validator(value):
    valid_extensions_file = ('pdf', 'png', 'jpeg', 'jpg')
    try:
        if value:
            file_name = value.name
            file_extension = file_name.split('.')[-1].lower()
            if file_extension in valid_extensions_file:
                if value.size > int(settings.MAX_UPLOAD_SIZE):
                    raise ValidationError(
                        'Please keep the file size under 10 MB'
                    )
            else:
                raise ValidationError(
                    'Please upload file in PDF/PNG/JPG/JPEG formats.'
                )
    except Exception:
        return True


def image_extension_validator(value):
    valid_extensions_image = ('png', 'jpeg', 'jpg')
    try:
        if value:
            image_name = value.name
            image_file_extension = image_name.split('.')[-1].lower()
            if image_file_extension in valid_extensions_image:
                if value.size > int(settings.MAX_UPLOAD_SIZE):
                    raise ValidationError(
                        'Please keep the file size under 10 MB'
                    )
            else:
                raise ValidationError(
                    'Please upload image in PNG/JPG/JPEG formats.'
                )
    except Exception:
        return True


def source_validation(value):
    """
        Valid sources for setting AMS unique IDs for users.
    """
    if value not in settings.VALID_SOURCES:
        raise ValidationError('Enter a valid source.')


def validate_email(email):
    """
        Create a hash of the email and check the uniqueness of the said email
        in the database.
    """
    if email:
        qs_filter = get_user_model().objects.filter(
            email=email
        )
        if qs_filter.exists():
            raise ValidationError('A user with this email already exists.')


def validate_mobile(mobile):
    """
        Mobile number validations.
    """
    if mobile:
        try:
            int(mobile)
        except ValueError:
            raise ValidationError('Please enter a valid mobile number')
        except TypeError:
            raise ValidationError('Please enter a valid mobile number')

        if mobile[0] not in ('6', '7', '8', '9'):
            raise ValidationError(
                'Mobile numbers must start with 6, 7, 8 or 9'
            )

        if len(mobile) != 10:
            raise ValidationError(
                'Length of a mobile number must be 10 digits'
            )

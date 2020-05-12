from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from apnaschool.accounts.models import Student

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    # first_name = forms.CharField(widget=forms.TextInput(), strip=True)
    # last_name = forms.CharField(widget=forms.TextInput(), strip=True)
    email = forms.EmailField(
        widget=forms.EmailInput(),
        error_messages={
            'required': 'Enter the Email ID.'
        }
    )

    password1 = forms.CharField(
        label=_('Password'),
        min_length=6,
        required=False,
        error_messages={
            'required': 'Enter New Password.',
            'min_length': 'Password should have minimum 6 characters.'
        },
        widget=forms.PasswordInput)

    password2 = forms.CharField(
        label=_('Password confirmation'),
        min_length=6,
        required=False,
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as above, for verification.'))

    def __int__(self):
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Student
        fields = ('email',)

    def clean_hashed_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.
        email = self.cleaned_data['email']
        try:
            UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(get_random_string())
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

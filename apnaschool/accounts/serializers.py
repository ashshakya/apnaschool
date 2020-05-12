from rest_framework import serializers

from apnaschool.accounts.models import Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'unique_code',
            'email',
            'standard',
            'is_fee_paid',
        )
        write_only_fields = (
            'unique_code'
        )
        read_only_fields = ('password',)

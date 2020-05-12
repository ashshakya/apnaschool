from rest_framework import serializers

from apnaschool.accounts.serializers import StudentSerializer
from apnaschool.accounts.models import Student
from apnaschool.ops.models import Transactions
from apnaschool.data.serializers import FeeStructureSerializer

# from apnaschool.ops.serializers import FeeStructureSerializer

# class StudentSerializer(serializers.ModelSerializer):

#     pass


class TransactionSerializer(serializers.ModelSerializer):

    # student = serializers.CharField()
    # student = StudentSerializer()

    tution_fee = FeeStructureSerializer(required=False)

    class Meta:
        model = Transactions
        fields = (
            # 'student',
            'tution_fee',
            'pending_balance',
            'concession',
            'other_charges',
            'remarks',
            'receipt_no',
            'created_at',
        )

    def create(self, validated_data):
        student = Student.objects.get(
            unique_code=validated_data.pop('student')
        )
        txn = Transactions.objects.create(
            student=student, **validated_data
        )
        return txn


class StudentFeeSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    unique_code = serializers.CharField(max_length=10)
    standard = serializers.CharField(max_length=10)
    category = serializers.CharField(max_length=50)

    transaction = TransactionSerializer(source='transaction_set')

    class Meta:
        model = Student
        fields = (
            'full_name', 'unique_code', 'standard', 'category',
            'transaction'
        )

    def get_full_name(self, obj):
        return obj.get_full_name()

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework.views import APIView

from rest_framework.response import Response

from apnaschool.accounts.models import Student
from apnaschool.data.models import Standard
from apnaschool.utils import timezone
from apnaschool.ops.models import Transactions
from apnaschool.accounts.serializers import StudentSerializer
from apnaschool.ops.serializers import TransactionSerializer, StudentFeeSerializer


RECORD_PER_PAGE = 25


class GetStudentDetails(APIView):

    def get_queryset(self):
        search_filter = Q()
        search = self.request.GET.get('search', '')
        standard = self.request.GET.get('standard', None)
        search_parts = search.split(' ')
        for part in search_parts:
            q = Q(
                Q(first_name__icontains=part) |
                Q(last_name__icontains=part) |
                Q(middle_name__icontains=part) |
                Q(email__icontains=part) |
                Q(unique_code__icontains=part)
            )
            search_filter = search_filter | q if search_filter else q

        student = Student.objects.filter(
            search_filter
        )
        if standard:
            student = student.filter(standard=standard)
        return student

    def get(self, request):
        serializer = StudentSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class TransactionView(APIView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Standard.objects.all()
        return context

    def get(self, request, pk=None):

        try:
            student = Student.objects.get(id=pk)

        except Exception:
            return Response({
                'error': 'Student Does Not Exists.'
            })
        # txn = Transactions.objects.all()
        serializer = StudentFeeSerializer(student)

        return Response(serializer.data)

    def post(self, request):

        serializer = TransactionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

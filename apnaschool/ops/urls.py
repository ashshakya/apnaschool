from django.urls import path, re_path

from apnaschool.ops.views import TransactionView, GetStudentDetails

# router = DefaultRouter()
# router.register('transaction', TransactionView)

urlpatterns = [
    path(
        r'pay/', TransactionView.as_view(), name='pay-fee'
    ),
    path(
        r'search/', GetStudentDetails.as_view(), name='search'
    ),
    re_path(r'^pay_fee/(?P<pk>.+)/$', TransactionView.as_view(), name='pay-fee')
]

from django.urls import path
from .views import add_reservation_view, reservation_detail_view, PaymentSuccess, PaymentFailed

urlpatterns = [
    path('<vehicle_id>/', add_reservation_view, name="reserve"),
    path('detail/<reservation_id>/', reservation_detail_view, name="reserve_detail"),
    path('pay-success/<int:reservation_id>', PaymentSuccess.as_view(), name='success_pay'),
    path('pay-failed/<int:reservation_id>', PaymentFailed.as_view(), name='failed_pay'),
]

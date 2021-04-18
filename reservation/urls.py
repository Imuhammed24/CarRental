from django.urls import path
from .views import add_reservation_view, reservation_detail_view, PaymentSuccess, PaymentFailed, \
    reservation_list_view

urlpatterns = [
    path('<vehicle_id>/', add_reservation_view, name="reserve"),
    path('detail/<reservation_id>/', reservation_detail_view, name="reserve_detail"),
    path('list', reservation_list_view, name="reservation_list"),
    path('pay-success/<int:reservation_id>', PaymentSuccess.as_view(), name='success_pay'),
    path('pay-failed/<int:reservation_id>', PaymentFailed.as_view(), name='failed_pay'),
]

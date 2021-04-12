from django.urls import path
from .views import add_reservation_view, reservation_detail_view

urlpatterns = [
    path('<vehicle_id>/', add_reservation_view, name="reserve"),
    path('detail/<reservation_id>/', reservation_detail_view, name="reserve_detail"),
]

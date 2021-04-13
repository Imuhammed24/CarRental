from django.urls import path
from .views import send_message_view


urlpatterns = [
    path('send-message/<vehicle_id>/', send_message_view, name="send_message"),
]
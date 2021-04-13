import django
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from . import settings
from . import views

app_name = 'paystack'

urlpatterns = [
    path("webhook/", views.webhook_endpoint, name="webhook"),

    path("verify-payment/<reservation_id>/", views.verify_payment, name="verify_payment"),

    path(
        "failed-verification/<order_id>/", views.failure_redirect_view,
        name="failed_verification",),

    path("successful-verification/<reservation_id>/", views.success_redirect_view,
         name="successful_verification",),

    path("failed-page/",
         TemplateView.as_view(template_name="paystack/failed-page.html"),
         name="failed_page",),

    path("success-page/<order_id>/",
         TemplateView.as_view(template_name="paystack/success-page.html"),
         name="success_page",),

    # path("webhook/", csrf_exempt(views.webhook_view), name="webhook"),
]

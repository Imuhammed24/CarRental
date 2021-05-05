import json
import hmac
import hashlib
from django.shortcuts import redirect, reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.generic import RedirectView
from . import settings, signals
from .signals import payment_verified
from .utils import load_lib
from .models import PaymentHistory


def verify_payment(request, reservation_id):
    amount = request.GET.get('amount')
    txrf = request.GET.get('transaction_ref')
    paystack_api = load_lib()
    paystack_instance = paystack_api()
    response = paystack_instance.verify_payment(txrf, amount=int(amount))
    if response[0]:
        payment_verified.send(
            sender=paystack_api,
            ref=txrf,
            amount=int(amount) / 100,
            order=reservation_id)
        return redirect(
            reverse('paystack:successful_verification', args=[reservation_id]))
    return redirect(reverse('paystack:failed_verification', args=[reservation_id]))


class FailedView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_FAILED_URL == 'paystack:failed_page':
            return reverse(settings.PAYSTACK_FAILED_URL)
        return settings.PAYSTACK_FAILED_URL


def success_redirect_view(request, reservation_id):
    url = settings.PAYSTACK_SUCCESS_URL
    if url == 'reservation:success_pay':
        url = reverse(url, args=[reservation_id])
    return redirect(url, permanent=True)


def failure_redirect_view(request, order_id):
    url = settings.PAYSTACK_FAILED_URL
    if url == 'reservation:failed_pay':
        url = reverse(url, args=[order_id])
    return redirect(url, permanent=True)


class SuccessView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if not settings.PAYSTACK_SUCCESS_URL:
            return reverse('paystack:success_page')
        return settings.PAYSTACK_SUCCESS_URL


def payment_state():
    """ Keep payment information state. """
    p_event = None
    p_payment_date = None
    p_reference = None
    p_email = None
    p_json_body = None


def update_payment(json_body):
    """Update payment status based on data from json_body."""
    print('UPDATING PAYMENT')
    event = json_body['event']
    new_data = json_body['data']
    reference = new_data['reference']
    email = new_data['customer']['email']
    # metadata = new_data['customer']['metadata']
    # print(metadata)
    payment_date = new_data['paid_at']
    if event == 'charge.success':
        from reservation.models import Reservation
        reservation = Reservation.objects.get(id=reference)
        reservation.is_paid = True
        reservation.vehicle.quantity -= 1
        if reservation.vehicle.quantity == 0:
            reservation.vehicle.availability = False
        reservation.vehicle.save()
        reservation.save()

        PaymentHistory.objects.create(
            email=email,
            reference=reference, data=json_body
        )

        payment_state.p_event = event
        payment_state.p_payment_date = payment_date
        payment_state.p_reference = reference
        payment_state.p_email = email
        payment_state.p_json_body = json_body

    else:
        PaymentHistory.objects.create(
            email=email,
            reference=reference,
            data=json_body
        )
        payment_state.p_event = event
        payment_state.p_payment_date = payment_date
        payment_state.p_reference = reference
        payment_state.p_email = email
        payment_state.p_json_body = json_body


@require_POST
@csrf_exempt
def webhook_endpoint(request):
    """
    The function takes an http request object
    containing the json data from paystack webhook client.
    Django's http request and response object was used
    for this example.
    """
    paystack_sk = settings.PAYSTACK_SECRET_KEY
    json_body = json.loads(request.body)
    computed_hmac = hmac.new(
        bytes(paystack_sk, 'utf-8'),
        str.encode(request.body.decode('utf-8')),
        digestmod=hashlib.sha512
        ).hexdigest()

    if 'HTTP_X_PAYSTACK_SIGNATURE' in request.META:
        if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == computed_hmac:
            update_payment(json_body)
            payload = json_body
            signals.event_signal.send(
                sender=request, event=payload['event'], data=payload['data'])
            return HttpResponse(status=200)

    # Not successful
    update_payment(json_body)
    payload = json_body
    signals.event_signal.send(
        sender=request, event=payload['event'], data=payload['data'])

    return HttpResponse(status=400)  # non 200

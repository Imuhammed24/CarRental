import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView

from reservation.forms import ReservationForm
from reservation.models import Reservation
from vehicles.forms import MessagesForm
from vehicles.models import Vehicle, Messages
from paystack.views import payment_state


def add_reservation_view(request, vehicle_id):
    if request.user.is_authenticated:
        admin = User.objects.get(username='admin')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        chat = Messages.objects.filter(vehicle=vehicle,
                                       sender__in=[request.user, admin],
                                       receiver__in=[request.user, admin])
        context = {
            'html_title': f'RESERVE {vehicle.brand.name.upper()}',
            'vehicle': vehicle,
            'chat': chat,
            'message_form': MessagesForm(),
            'section': 'account',
            'sub_section': 'reserve',
        }
        if request.method == 'POST':
            reservation_form = ReservationForm(request.POST)
            if reservation_form.is_valid():
                new_reservation = reservation_form.save(commit=False)
                new_reservation.user = request.user
                new_reservation.vehicle = vehicle
                vehicle.quantity -= 1
                if vehicle.quantity == 0:
                    vehicle.availability = False
                vehicle.save()
                new_reservation.save()
                context['is_reserved'] = True
                context['reservation'] = new_reservation
            else:
                messages.error(request, 'Error! Invaild input.')
            return render(request, 'account/account_base.html', context)
        else:
            context['reservation_form'] = ReservationForm()
            return render(request, 'account/account_base.html', context)
    else:
        messages.error(request, 'Please login')
        return redirect('index')


@login_required(login_url='/')
def reservation_detail_view(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    vehicle = reservation.vehicle
    context = {
        'html_title': f'RESERVATION DETAILS {vehicle.brand}',
        'reservation': reservation,
        'vehicle': vehicle,
        'section': 'account',
        'sub_section': 'reservation_detail',
    }
    return render(request, 'account/account_base.html', context)


@login_required(login_url='/')
def reservation_list_view(request):
    # delete expired reservations
    expired_reservations = request.user.reservations.filter(expiry__lte=timezone.now())
    if expired_reservations:
        for expired_reservation in expired_reservations:
            expired_reservation.vehicle.quantity += 1
            expired_reservation.vehicle.save()
            expired_reservation.delete()

    reservations = Reservation.objects.filter(user=request.user)
    reservations = [reservation for reservation in reservations if
                    reservation.expiry > timezone.now() or reservation.is_paid is True]
    # reservations = request.user.reservations.fil(expiry__lte=datetime.datetime.now())
    context = {
        'html_title': 'RESERVATIONS',
        'reservations': reservations,
        'section': 'account',
        'sub_section': 'reservation_list',
    }
    return render(request, 'account/account_base.html', context)


class PaymentSuccess(TemplateView):
    """Land here on successful payment verification."""
    template_name = 'paystack/success-page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        reservation_id = kwargs['reservation_id']

        reservation = Reservation.objects.get(id=reservation_id)

        # state = [{'event': payment_state.p_event}, payment_state.p_payment_date,
        #          payment_state.p_reference, payment_state.p_email, payment_state.p_json_body]

        # context['paystate'] = state
        context['reservation'] = reservation
        context['tracking_id'] = reservation_id
        context['sub_section'] = 'payment_success'
        context['section'] = 'account'
        context['html_title'] = 'PURCHASE SUCCESSFUL'
        return context


class PaymentFailed(TemplateView):
    """Land here on failed payment verification."""
    template_name = 'paystack/success-page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        reservation_id = kwargs['reservation_id']

        reservation = Reservation.objects.get(id=reservation_id)

        state = [{'event': payment_state.p_event}, payment_state.p_payment_date,
                 payment_state.p_reference, payment_state.p_email, payment_state.p_json_body]

        context['paystate'] = state
        context['order'] = reservation
        context['tracking_id'] = reservation_id
        context['html_title'] = 'PURCHASE FAILED'
        return context

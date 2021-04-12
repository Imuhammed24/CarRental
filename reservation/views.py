from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from reservation.forms import ReservationForm
from reservation.models import Reservation
from vehicles.models import Vehicle


@login_required(login_url='/')
def add_reservation_view(request, vehicle_id):
    if request.user.is_authenticated:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        context = {
            'html_title': f'RESERVE {vehicle.brand}',
            'vehicle': vehicle,
            'section': 'reserve',
        }
        if request.method == 'POST':
            reservation_form = ReservationForm(request.POST)
            if reservation_form.is_valid():
                new_reservation = reservation_form.save(commit=False)
                new_reservation.user = request.user
                new_reservation.vehicle = vehicle
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
        'section': 'reservation_detail',
    }
    return render(request, 'account/account_base.html', context)

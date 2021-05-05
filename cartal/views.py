from django.shortcuts import render

from account.forms import UserRegistrationForm, LoginForm, ProfileForm
from vehicles.models import Vehicle


def index_view(request):
    registration_form = UserRegistrationForm()
    profile_form = ProfileForm()
    login_form = LoginForm()
    if request.user.is_authenticated:
        reservations = request.user.reservations.all()
        vehicles = Vehicle.objects.all().exclude(id__in=[vehicle.id for vehicle in reservations])
    else:
        vehicles = Vehicle.objects.all()
    context = {
        'registration_form': registration_form,
        'profile_form': profile_form,
        'login_form': login_form,
        'vehicles': vehicles,
        'html_title': 'WELCOME TO CARTAL',
    }
    return render(request, 'index.html', context)


def contact_view(request):
    return render(request, 'contact.html', {})


def about_view(request):
    return render(request, 'about.html', {})

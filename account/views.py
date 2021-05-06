import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST

from account.forms import UserRegistrationForm, LoginForm, ProfileForm
from vehicles.models import Vehicle


def validate_digits_letters(word):
    for char in word:
        if not char.isdigit() and not char.isalpha() and not char in ['@', '.']:
            return False
    return True


def register_view(request):
    reg_form = UserRegistrationForm(request.POST)
    profile_form = ProfileForm(request.POST)
    login_form = LoginForm()

    if request.method == 'POST':
        if reg_form.is_valid() and profile_form.is_valid():
            new_user = reg_form.save(commit=False)
            new_user_profile = profile_form.save(commit=False)
            new_user.set_password(
                reg_form.cleaned_data['password']
            )
            new_user.is_active = True
            new_user.save()
            new_user_profile.user = new_user
            new_user_profile.save()
            messages.success(request, 'Account created successfully!')

            return redirect('index')

        else:
            messages.error(request, f'{reg_form.errors}')
            return redirect('index')

    else:
        messages.error(request, 'Error registering, please try again.')
        return redirect('index')


@require_POST
def login_view(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = str(request.POST.get('username')).lower()
        password = str(request.POST.get('password'))

        if (len(username) > 45 or len(password) > 45) or \
                (len(username) == 0 or len(password) == 0) or \
                (not validate_digits_letters(username)):
            messages.error(request, 'Error, invalid characters!')
            return redirect('index')

        user = authenticate(request=request,
                            username=username,
                            password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return redirect('account:home')
                # return HttpResponse('Logged in')
        else:
            messages.error(request, 'Login Failed. Plaese check username or password supplied.')
            return redirect('index')
    else:
        messages.error(request, 'Invalid Login. Please try again')
        return redirect('index')


def home_view(request):
    # delete expired reservations
    if request.user.is_authenticated:
        expired_reservations = request.user.reservations.filter(expiry__lte=timezone.now())
        if expired_reservations:
            for expired_reservation in expired_reservations:
                expired_reservation.vehicle.quantity += 1
                expired_reservation.vehicle.save()
                expired_reservation.delete()
        # vehicles = Vehicle.objects.all().exclude(id__in=[vehicle.id for vehicle in reservations])
        vehicles = Vehicle.objects.filter(quantity__gte=1, availability=True)
        context = {
            'html_title': f'{request.user.username.upper()} ACCOUNT',
            'vehicles': vehicles,
            'section': 'account',
            'sub_section': 'default_home',
        }
        return render(request, 'account/account_base.html', context)
    else:
        messages.error(request, 'please login')
        return redirect('index')


@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('account:home')


@login_required(login_url='/')
def profile_view(request):
    context = {
        'section': 'account',
        'sub_section': 'profile',
    }
    return render(request, 'account/account_base.html', context)

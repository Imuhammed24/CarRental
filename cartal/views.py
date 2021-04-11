from django.shortcuts import render

from account.forms import UserRegistrationForm, LoginForm, ProfileForm


def index_view(request):
    registration_form = UserRegistrationForm()
    profile_form = ProfileForm()
    login_form = LoginForm()
    context = {
        'registration_form': registration_form,
        'profile_form': profile_form,
        'login_form': login_form,
        'html_title': 'WELCOME TO CARTAL',
    }
    return render(request, 'index.html', context)

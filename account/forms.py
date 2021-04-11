from django import forms
from django.contrib.auth.models import User

from account.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username/Email')
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('passwords don\'t match')
        return cd['confirm_password']


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(label='Full Name',
                                widget=forms.TextInput(attrs={'placeholder': 'First Name    Last Name'}))

    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number']

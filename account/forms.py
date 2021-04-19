from django import forms
from django.contrib.auth.models import User

from account.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username/Email', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), max_length=20)
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('passwords don\'t match')
        return cd['confirm_password']

    def clean_email(self):
        cd = self.cleaned_data
        emails = [user.email for user in User.objects.all()]
        if cd['email'] in emails:
            raise forms.ValidationError('email has been used by another user')
        else:
            return cd['email']


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(label='Full Name',
                                widget=forms.TextInput(attrs={'placeholder': 'First Name    Last Name'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}), max_length=15)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}), max_length=15)

    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'address']

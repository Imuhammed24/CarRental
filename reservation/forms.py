from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput
from reservation.models import Reservation


class ReservationForm(forms.ModelForm):
    # start_period = forms.DateTimeField(widget=DateTimePickerInput())
    # end_period = forms.DateTimeField(widget=DateTimePickerInput())

    class Meta:
        model = Reservation
        fields = ['start_period', 'end_period']
        widgets = {
            'start_period': DateTimePickerInput().start_of('start_period'),
            'end_period': DateTimePickerInput().end_of('start_period'),
        }

from django import forms
from vehicles.models import Messages


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }

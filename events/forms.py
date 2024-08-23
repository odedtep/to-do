from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'start_date', 'end_date', 'start_time',
            'end_time', 'category', 'location', 'visibility', 'invited_users',
            'payment_type', 'payment_amount',
            'image',
            'video',
        ]
        widgets = {
            'invited_users': forms.CheckboxSelectMultiple(),
            'payment_amount': forms.NumberInput(attrs={'step': '0.10', 'min': '0'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
            'video': forms.ClearableFileInput(attrs={'multiple': False}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_payment_amount(self):
        payment_amount = self.cleaned_data.get('payment_amount')
        if payment_amount is not None and payment_amount < 0:
            raise forms.ValidationError("Payment amount cannot be negative.")
        return payment_amount

    def clean(self):
        cleaned_data = super().clean()
        payment_type = cleaned_data.get("payment_type")
        payment_amount = cleaned_data.get("payment_amount")

        if payment_type != Event.NO_PAYMENT and not payment_amount:
            self.add_error('payment_amount', "Payment amount is required for this payment type.")
        elif payment_type == Event.NO_PAYMENT:
            cleaned_data['payment_amount'] = None

        return cleaned_data
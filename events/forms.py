from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description','start_date', 'end_date', 'start_time', 'end_time', 'category', 'location' ]
        widgets = {'invited_users': forms.CheckboxSelectMultiple()}

        #to add: 'start_date', 'end_date', 'start_time', 'end_time', 'category', 'location',
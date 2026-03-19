from django import forms
from .models import Trip
from network.models import Node

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['start_node', 'end_node', 'max_passengers']
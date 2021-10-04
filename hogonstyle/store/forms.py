from django import forms
from .models import SHIRT_SIZE_CHOICES, Item


class ForensicTrafficForm(forms.ModelForm):
    size = forms.CharField(widget=forms.RadioSelect(choices=SHIRT_SIZE_CHOICES))
    class Meta:
        model = Item
        fields = ['size']

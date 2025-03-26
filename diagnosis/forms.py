from django import forms
from .models import DermaCase

class DermaCaseForm(forms.ModelForm):
    class Meta:
        model = DermaCase
        fields = ['image', 'description']
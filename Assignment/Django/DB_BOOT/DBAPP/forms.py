from django import forms
from .models import *

class StudInfoForm(forms.ModelForm):
    class Meta:
        model=Studinfo
        fields='__all__'
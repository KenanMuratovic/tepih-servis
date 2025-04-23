from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Tepih, Zakazivanje

class CustomUserCreationForm(UserCreationForm):
    ime = forms.CharField(max_length=50)
    prezime = forms.CharField(max_length=50)
    email = forms.EmailField()
    broj_telefona = forms.CharField(max_length=20)
    lokacija = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['ime', 'prezime', 'email', 'password1', 'password2']

class TepihForm(forms.ModelForm):
    class Meta:
        model = Tepih
        fields = ['vrsta', 'velicina_m2', 'napomena']

class ZakazivanjeForm(forms.ModelForm):
    class Meta:
        model = Zakazivanje
        fields = ['datum']
        widgets = {
            'datum': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            })
        }

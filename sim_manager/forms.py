from django import forms
from .models import Simulation
from django.contrib.auth.models import User


class SimuForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = '__all__'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

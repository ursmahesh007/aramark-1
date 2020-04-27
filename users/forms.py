# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name',
                    'age', 'gender', 'height', 'weight',
                    'activity']

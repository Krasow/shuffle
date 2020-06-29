from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AccountForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "username", "password1", "password2"]

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User as Auth_User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import User
from django.forms import ModelForm


class CreateUserForm(UserCreationForm):

    class Meta:
        model = Auth_User
        fields = ['username', 'password1', 'password2']


class CreateUserInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','email','phone']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


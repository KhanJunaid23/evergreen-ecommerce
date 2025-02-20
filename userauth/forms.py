from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput({"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput({"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput({"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput({"placeholder":"Confirm Password"}))
    class Meta:
        model = User
        fields = ['username','email']
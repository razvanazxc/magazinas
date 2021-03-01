from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from accounts.models import MyUser
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password1', 'password2' ]

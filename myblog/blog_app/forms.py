from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "first_name", "last_name"


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = "first_name", "last_name", "email"


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = "bio", "avatar"

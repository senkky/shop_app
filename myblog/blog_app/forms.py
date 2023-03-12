from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm
from .models import Profile
from django import forms


class CreationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar',)


class UserRegisterMultiForm(MultiModelForm):
    form_classes = {
        'user': UserCreationForm,
        "profile": CreationProfileForm,
    }

    def save(self, commit=True):
        objects = super(UserRegisterMultiForm, self).save(commit=False)

        if commit:
            user = objects['user']
            user.save()
            profile = objects['profile']
            profile.user = user
            profile.save()

        return objects


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "first_name", "last_name"


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar",)


class UserProfileUpdateForm(MultiModelForm):
    form_classes = {
        'user': UserUpdateForm,
        'profile': ProfileUpdateForm,
    }

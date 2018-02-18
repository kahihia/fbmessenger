#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Avatar, FacebookAccount, FacebookProfileUrl


class SignupForm(UserCreationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(
                                   {'class':'form-control input-no-border',
                                    'placeholder': 'Enter username'}),
                               max_length=50, required=True)
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control input-no-border',
                                           'placeholder': 'Enter password',}))
    password2 = forms.CharField(label="Confirm password",
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control input-no-border',
                                           'placeholder': 'Confirm password',}))
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(
                                 attrs={'class':'form-control input-no-border',
                                        'placeholder': 'Enter email',}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'Enter first name'}), required=False)
    last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'Enter lat name'}), required=False)
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control border-input', 'placeholder': 'Enter email'}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'Enter username'}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class FacebookAccountForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'Enter username'}))
    password = forms.CharField(label="Current password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control border-input'}), required=False)

    class Meta:
        model = FacebookAccount
        fields = ("username", "password")


class FacebookProfileForm(forms.ModelForm):

    url = forms.URLField(label="Url", required=True,
                         widget=forms.URLInput(attrs={"class": "form-control broder-input",
                                                      "placeholder": "Enter url: http://"}))

    class Meta:
        model = FacebookProfileUrl
        fields = ("url",)


class BulkUrlform(forms.Form):
    url = forms.CharField(label="URLs", required=True,
                          widget=forms.Textarea(attrs={"class": "form-control",
                                                       "placeholder": "Input bulk URLs"}))


class PasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label="Current password",
                                   widget=forms.PasswordInput(attrs={'class': 'form-control border-input'}), required=False)
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control border-input'}), required=False)
    new_password2 = forms.CharField(label="Confirm password",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control border-input'}), required=False)


class UserAvatarForm(forms.ModelForm):

    image = forms.FileField(label="Avatar", required=False,
                            widget=forms.ClearableFileInput(attrs={'class': 'form-control border-input',
                                                                   'multiple': False,
                                                                   'accept': 'image/*'}))
    class Meta:
        model = Avatar
        fields = ("image", )

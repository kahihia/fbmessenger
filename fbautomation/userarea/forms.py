#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User


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

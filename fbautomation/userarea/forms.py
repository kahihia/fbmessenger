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
    first_name = forms.CharField(label="First name", required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control border-input',
                                            'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label="Last name", required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control border-input',
                                           'placeholder': 'Enter lat name'}))
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control border-input',
                                        'placeholder': 'Enter email'}))
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control border-input',
                                          'placeholder': 'Enter username'}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class FacebookAccountForm(forms.ModelForm):
    fb_user = forms.CharField(label="Username", required=True,
                           widget=forms.TextInput(
                                   attrs={'class': 'form-control border-input',
                                          'placeholder': 'Enter username'}))
    fb_pass = forms.CharField(label="Current password",required=True,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control border-input'}))

    class Meta:
        model = FacebookAccount
        fields = ("fb_user", "fb_pass")


class FacebookProfileForm(forms.ModelForm):
    tag = forms.CharField(label="Tag", required=True,
                           widget=forms.TextInput(
                                   attrs={'class': 'form-control border-input',
                                          'placeholder': 'Enter tag'}))

    url = forms.URLField(label="Url", required=True,
                         widget=forms.URLInput(
                             attrs={"class": "form-control broder-input",
                                    "placeholder": "Enter url: http://"}))

    class Meta:
        model = FacebookProfileUrl
        fields = ("tag", "url",)


class BulkUrlform(forms.Form):
    tag = forms.CharField(label="Tag", required=True,
                           widget=forms.TextInput(
                                   attrs={'class': 'form-control border-input',
                                          'placeholder': 'Enter tag'}))
    url = forms.CharField(label="URLs", required=True,
                          widget=forms.Textarea(
                              attrs={"class": "form-control",
                                     "placeholder": "Input bulk URLs"}))


class PasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label="Current password", required=False,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control border-input'}))
    new_password1 = forms.CharField(label="New password", required=False,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control border-input'}))
    new_password2 = forms.CharField(label="Confirm password", required=False,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control border-input'}))


class UserAvatarForm(forms.ModelForm):

    image = forms.FileField(label="Avatar", required=False,
                            widget=forms.ClearableFileInput(
                                attrs={'class': 'form-control border-input',
                                       'multiple': False,
                                       'accept': 'image/*'}))
    class Meta:
        model = Avatar
        fields = ("image", )


class MessageForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        # request is a required parameter for this form.
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["recipients"].queryset = FacebookProfileUrl.objects.filter(user=user,
                                                                               is_messaged=False,
                                                                               is_deleted=False)
    task_name = forms.CharField(label="Task name",
                                widget=forms.TextInput(
                                    attrs={
                                        "class": "form-control",
                                        "placeholde": "Enter task name",
                                    }))

    recipients = forms.ModelMultipleChoiceField(required=True,
                                                queryset=FacebookProfileUrl.objects.all(),
                                                widget=forms.SelectMultiple(
                                                    attrs={'class': 'form-control input-no-border selectpicker',
                                                           'data-actions-box': 'true',
                                                           'data-live-search': 'true',
                                                           'data-size': '5',
                                                           'title': 'Select recipients'}))
    message = forms.CharField(label="Message", required=True,
                              widget=forms.Textarea(
                                  attrs={"class": "form-control",
                                         "placeholder": "Enter message",
                                         "rows": 12}))





from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )

#  Copyright 2020 Julián Novoa Martín
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import RadioSelect

from .models import PredictionModels


class RegisterForm(UserCreationForm):
    """ Formulary designed to create a user """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    """ Formulary designed to log a user """
    remember_me = forms.BooleanField(label="Remember me", required=False)


class PredictionModelForm(forms.Form):
    """ Formulary designed to change the prediciton model """
    selected_prediction_model = forms.ChoiceField(choices=[(model.name, model.value) for model in PredictionModels],
                                                  widget=RadioSelect)


class EmailChangeForm(forms.Form):
    """ Formulary designed to change the user's email """
    error_messages = {
        'email_mismatch': "The two email addresses fields didn't match.",
        'not_changed': "The email address is the same as the one already defined.",
    }

    new_email1 = forms.EmailField(
        label="New email address",
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label="New email address confirmation",
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user

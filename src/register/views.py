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
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import descriptions, more_info
from .forms import RegisterForm, LoginForm, PredictionModelForm, EmailChangeForm


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usr = form.save()
            login(request, usr)
            return redirect(reverse('profile'))
    else:
        form = RegisterForm()

    return render(request, 'register/register.html', {'form': form})


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'register/login.html'
    authentication_form = LoginForm


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('changedata')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'register/changepswd.html', {'form': form})


@login_required
def change_email_view(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('changedata')
    else:
        form = EmailChangeForm(request.user)
    return render(request, 'register/changemail.html', {'form': form})


@login_required
def change_prediction_model_view(request):
    if request.method == 'POST':
        form = PredictionModelForm(request.POST)
        if form.is_valid():
            usr = request.user
            usr.settings.prediction_model = form.cleaned_data['selected_prediction_model']
            usr.settings.save()
            return redirect('changedata')
    else:
        form = PredictionModelForm()

    return render(request, 'register/changepm.html', {'pm': request.user.settings.prediction_model,
                                                      'form': form,
                                                      'description': descriptions,
                                                      'url': more_info})



@login_required
def remove_user_view(request):
    usr = get_object_or_404(User, pk=request.user.pk)
    try:
        usr.delete()
    except Exception:
        return HttpResponseServerError('Error. User was not removed.')

    return redirect('initial')

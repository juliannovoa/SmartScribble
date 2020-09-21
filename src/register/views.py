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
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm, PredictionModelForm


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            usr = form.save()
            return render(request, "pages/profile.html", context={'user': usr})
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})


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
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'register/changepswd.html', {'form': form})


@login_required
def change_prediction_model_view(request):
    if request.method == "POST":
        form = PredictionModelForm(request.POST)
        print(request.POST['selected_prediction_model'])
        if form.is_valid():
            usr = request.user
            prediction_model = form.cleaned_data['selected_prediction_model']
            usr.settings.prediction_model = prediction_model
            usr.save()
    else:
        form = PredictionModelForm()
        prediction_model = request.user.settings.prediction_model

    return render(request, 'register/changepm.html', {'pm': prediction_model, 'form': form})

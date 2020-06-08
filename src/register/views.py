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
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import RegisterForm, LoginForm


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            usr = form.save()
            return render(request, "register/successfulRegister.html", context={'user': usr})
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})


def login_view(request):
    return render(request, "register/login.html")


class CustomLoginView(LoginView):
    template_name = 'register/login.html'
    authentication_form = LoginForm

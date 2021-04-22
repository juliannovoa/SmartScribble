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

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from document.views import remove_document_view, edit_document_view, predict_view, full_predict_view
from pages.views import profile_view, change_data_view
from register.views import register_view, CustomLoginView, change_password_view, change_prediction_model_view, change_email_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', CustomLoginView.as_view(), name='initial'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('remove/', remove_document_view, name='remove'),
    path('edit/', edit_document_view, name='edit'),
    path('changedata/', change_data_view, name='changedata'),
    path('changepswd/', change_password_view, name='changepswd'),
    path('predict/', predict_view, name='prediction'),
    path('full_predict/', full_predict_view, name='complete_prediction'),
    path('changepm/', change_prediction_model_view, name='changepm'),
    path('changemail/', change_email_view, name='changemail'),


]

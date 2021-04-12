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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from common.util import get_logged_users
from register.forms import RegisterForm, PredictionModelForm, LoginForm
from register.models import PredictionModels


class RegisterViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_user_not_logged(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/register.html')

    def test_view_redirects_user_logged(self):
        user = User.objects.create(username='test_user')
        self.client.force_login(user)
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))

    def test_form_create_user_is_correct(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))

    def test_initial_form_create_user_is_empty(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_view_creates_user(self):
        data = {'username': 'test_user',
                'email': 'example@email.com',
                'password1': 'qawsedrftgyh',
                'password2': 'qawsedrftgyh'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        try:
            User.objects.get(username='test_user')
        except User.DoesNotExist:
            self.fail('User does not exists.')

    def test_view_response_form_invalid_data(self):
        data = {'username': 'test_user',
                'email': 'example@email.com',
                'password1': 'qawsedrftgyh',
                'password2': 'qawsedgyh'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/register.html')

    def test_view_logs_user_after_create_it(self):
        data = {'username': 'test_user',
                'email': 'example@email.com',
                'password1': 'qawsedrftgyh',
                'password2': 'qawsedrftgyh'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        try:
            user = User.objects.get(username='test_user')
        except User.DoesNotExist:
            self.fail('User does not exists.')
        logged_users = get_logged_users()
        self.assertTrue(user in logged_users)

    def test_redirection_after_user_creation(self):
        data = {'username': 'test_user',
                'email': 'example@email.com',
                'password1': 'qawsedrftgyh',
                'password2': 'qawsedrftgyh'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/profile/'))


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.test_user.set_password('qawsedrftgyh')
        self.test_user.save()

    def test_redirect_if_not_logged(self):
        response = self.client.get('/changepswd/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/changepswd/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/changepswd.html')

    def test_form_change_password_is_correct(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordChangeForm))

    def test_initial_form_change_password_is_empty(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_view_change_password(self):
        self.client.force_login(self.test_user)
        new_password = 'newpassw_1!'
        data = {'old_password': 'qawsedrftgyh',
                'new_password1': new_password,
                'new_password2': new_password}

        response = self.client.post(reverse('changepswd'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('changedata'))
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password(new_password))

    def test_view_response_form_invalid_data(self):
        self.client.force_login(self.test_user)
        new_password = 'newpassw_1!'
        data = {'old_password': 'invalid',
                'new_password1': new_password,
                'new_password2': new_password}
        response = self.client.post(reverse('changepswd'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/changepswd.html')


class ChangePredictionModelViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.test_user.save()

    def test_redirect_if_not_logged(self):
        response = self.client.get('/changepm/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/changepm/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepm'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepm'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/changepm.html')

    def test_form_change_prediction_model_is_correct(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepm'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, PredictionModelForm))

    def test_initial_form_change_prediction_model_is_empty(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changepm'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_view_change_prediction_model(self):
        self.client.force_login(self.test_user)
        for model in PredictionModels:
            data = {'selected_prediction_model': model.name}
            self.assertTrue(PredictionModelForm(data).is_valid())
            response = self.client.post(reverse('changepm'), data)
            self.assertEqual(response.status_code, 302)
            self.test_user.refresh_from_db()
            self.assertEqual(self.test_user.settings.prediction_model, model.name)


class CustomLogInViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.test_user.set_password('qawsedrftgyh')
        self.test_user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_user_not_logged(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/login.html')

    def test_view_redirects_user_logged(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))

    def test_form_login_user_is_correct(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginForm))

    def test_initial_form_create_user_is_empty(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_view_logs_user(self):
        user_data = {'username': 'test_user',
                     'password': 'qawsedrftgyh'}
        logged_users_list = get_logged_users()
        self.assertFalse(self.test_user in logged_users_list)
        response = self.client.post(reverse('login'), user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        logged_users_list = get_logged_users()
        self.assertTrue(self.test_user in logged_users_list)

    def test_view_response_form_invalid_data(self):
        user_data = {'username': 'test_user',
                     'password': 'invalid'}
        logged_users_list = get_logged_users()
        self.assertFalse(self.test_user in logged_users_list)
        response = self.client.post(reverse('login'), user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/login.html')
        logged_users_list = get_logged_users()
        self.assertFalse(self.test_user in logged_users_list)

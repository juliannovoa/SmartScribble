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

from register.forms import RegisterForm


class RegisterViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user',
                                   password='qawsedrftgyh')
        user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_user_not_logged(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register/register.html")

    def test_view_redirects_user_logged(self):
        user = User.objects.get(username='test_user')
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
        data = {'username': 'test_user_2',
                'email': 'example@email.com',
                'password1': 'qawsedrftgyh',
                'password2': 'qawsedrftgyh'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='test_user_2')
        self.assertIsNotNone(user)
        self.assertTemplateUsed(response, "pages/profile.html")

    def test_view_response_form_invalid_data(self):
        data = {'username': 'test_user_2',
                'email': 'example@email.com',
                'password1': 'qawsedrftgyh',
                'password2': 'qawsedgyh'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register/register.html")


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user')
        user.set_password('qawsedrftgyh')
        user.save()

    def test_redirect_if_not_logged(self):
        response = self.client.get('/changepswd/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        response = self.client.get('/changepswd/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_user_not_logged(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register/changepswd.html")

    def test_form_change_password_is_correct(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordChangeForm))

    def test_initial_form_create_user_is_empty(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        response = self.client.get(reverse('changepswd'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_view_change_password(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        new_password = 'newpassw_1!'
        data = {'old_password': 'qawsedrftgyh',
                'new_password1': new_password,
                'new_password2': new_password}

        response = self.client.post(reverse('changepswd'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        user = User.objects.get(username='test_user')
        self.assertTrue(user.check_password(new_password))

    def test_view_response_form_invalid_data(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        new_password = 'newpassw_1!'
        data = {'old_password': 'invalid',
                'new_password1': new_password,
                'new_password2': new_password}
        response = self.client.post(reverse('changepswd'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register/changepswd.html")

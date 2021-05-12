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

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from document.forms import DocumentCreationForm
from document.models import Document


class ProfileViewTest(TestCase):
    @staticmethod
    def create_documents(user: User, number: int) -> set:
        documents_created = set()
        for i in range(number):
            doc = Document.objects.create(title='test_title',
                                          user=user)
            doc.save()
            documents_created.add(doc)
        return documents_created

    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.test_user.set_password('qawsedrftgyh')
        self.test_user.save()

    def test_redirect_if_not_logged(self):
        response = self.client.post(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('profile'))
        self.assertEqual(response.status_code, 500)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/profile.html')

    def test_form_create_user_is_correct(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, DocumentCreationForm))

    def test_initial_form_create_user_is_empty(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_view_shows_all_documents_of_the_user(self):
        self.client.force_login(self.test_user)
        documents_set = self.create_documents(self.test_user, 3)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        displayed_docs = set(response.context['docs'])
        self.assertEquals(displayed_docs, documents_set)

    def test_view_does_not_show_documents_of_other_users(self):
        self.client.force_login(self.test_user)
        self.create_documents(self.test_user, 3)
        new_user = User.objects.create(username='test_user_2')
        self.create_documents(new_user, 3)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        displayed_docs = set(response.context['docs'])
        for doc in Document.objects.exclude(user=self.test_user):
            self.assertFalse(doc in displayed_docs)

    def test_view_creates_documents(self):
        self.client.force_login(self.test_user)
        data = {'title': 'test_title',
                'description': 'test_description'}
        documents = Document.objects.filter(user=self.test_user)
        self.assertEqual(len(documents), 0)
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 302)
        documents = Document.objects.filter(user=self.test_user)
        self.assertEqual(len(documents), 1)
        doc = documents[0]
        self.assertEquals(doc.title, 'test_title')
        self.assertEquals(doc.description, 'test_description')


class ChangeDataViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.test_user.set_password('qawsedrftgyh')
        self.test_user.save()

    def test_redirect_if_not_logged(self):
        response = self.client.post(reverse('changedata'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/changedata/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('changedata'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('changedata'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/changedata.html')

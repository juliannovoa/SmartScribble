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

from document.forms import DocumentEditionForm
from document.models import Document


class RemoveDocumentViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.test_doc = Document.objects.create(title='test_title',
                                                user=self.test_user)

    def test_redirect_if_not_logged(self):
        response = self.client.post(reverse('remove'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.test_user)
        response = self.client.post('/remove/', {'doc_id': self.test_doc.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/profile/'))

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('remove'), {'doc_id': self.test_doc.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/profile/'))

    def test_document_does_not_exist(self):
        self.client.force_login(self.test_user)
        unavailable_doc_pk = 5
        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(pk=unavailable_doc_pk)
        response = self.client.post(reverse('remove'), {'doc_id': unavailable_doc_pk})
        self.assertEqual(response.status_code, 404)

    def test_document_does_not_belongs_to_logged_user(self):
        self.client.force_login(self.test_user)
        new_user = User.objects.create(username='test_user2')
        new_user.save()
        new_doc = Document.objects.create(title='test_title',
                                          user=new_user)
        new_doc.save()
        new_doc_pk = new_doc.pk
        response = self.client.post(reverse('remove'), {'doc_id': new_doc_pk})
        self.assertEqual(response.status_code, 403)

    def test_view_removes_document(self):
        self.client.force_login(self.test_user)
        doc_pk = self.test_doc.pk
        self.client.post(reverse('remove'), {'doc_id': doc_pk})
        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(pk=doc_pk)

    def test_view_rejects_get_request(self):
        self.client.force_login(self.test_user)
        doc_pk = self.test_doc.pk
        response = self.client.get(reverse('remove'), {'doc_id': doc_pk})
        self.assertEqual(response.status_code, 500)


class EditDocumentViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.test_doc = Document.objects.create(title='test_title',
                                                body='test_body',
                                                user=self.test_user)

    def test_redirect_if_not_logged(self):
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_view_url_exists_at_desired_location_with_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/edit/', {'id': self.test_doc.pk})
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_with_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('edit'), {'id': self.test_doc.pk})
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_with_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('edit'), {'id': self.test_doc.pk})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document/textEditor.html')

    def test_view_uses_correct_form_with_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('edit'), {'id': self.test_doc.pk})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, DocumentEditionForm))

    def test_view_uses_form_with_desired_data_with_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('edit'), {'id': self.test_doc.pk})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.initial["body"], 'test_body')

    def test_view_url_exists_at_desired_location_with_post(self):
        self.client.force_login(self.test_user)
        data = {'id': self.test_doc.pk,
                'body': 'new_body'}
        response = self.client.post('/edit/', data)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_with_post(self):
        self.client.force_login(self.test_user)
        data = {'id': self.test_doc.pk,
                'body': 'new_body'}
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_with_post(self):
        self.client.force_login(self.test_user)
        data = {'id': self.test_doc.pk,
                'body': 'new_body'}
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document/textEditor.html')

    def test_view_uses_correct_form_with_post(self):
        self.client.force_login(self.test_user)
        data = {'id': self.test_doc.pk,
                'body': 'new_body'}
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, DocumentEditionForm))

    def test_view_uses_form_with_desired_data_with_post(self):
        self.client.force_login(self.test_user)
        data = {'id': self.test_doc.pk,
                'body': 'new_body'}
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.initial["body"], 'new_body')

    def test_view_change_document(self):
        self.client.force_login(self.test_user)
        data = {'id': self.test_doc.pk,
                'body': 'new_body'}
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)
        document = Document.objects.get(pk=data['id'])
        self.assertEqual(document.body, 'new_body')

    def test_document_does_not_exist(self):
        self.client.force_login(self.test_user)
        unavailable_doc_pk = 5
        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(pk=unavailable_doc_pk)
        response = self.client.get(reverse('edit'), {'id': unavailable_doc_pk})
        self.assertEqual(response.status_code, 404)

    def test_document_does_not_belongs_to_logged_user(self):
        self.client.force_login(self.test_user)
        new_user = User.objects.create(username='test_user2')
        new_user.save()
        new_doc = Document.objects.create(title='test_title',
                                          user=new_user)
        new_doc.save()
        new_doc_pk = new_doc.pk
        response = self.client.post(reverse('edit'), {'id': new_doc_pk})
        self.assertEqual(response.status_code, 403)

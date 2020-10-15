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
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from document.forms import DocumentEditionForm
from document.models import Document
from register.models import PredictionModels


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


class PredictViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user')

    def test_redirect_if_not_logged(self):
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    @patch('document.views.PredictionService')
    def test_view_url_exists_at_desired_location_with_get(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'

        response = self.client.get('/predict/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    @patch('document.views.PredictionService')
    def test_view_url_accessible_by_name_with_get(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'

        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_view_throws_500_with_post_request(self):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }

        response = self.client.post(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 500)

    def test_view_throws_500_with_no_ajax_request(self):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }

        response = self.client.get(reverse('prediction'), data)
        self.assertEqual(response.status_code, 500)

    def test_view_throws_500_with_no_input_data_in_request(self):
        self.client.force_login(self.test_user)
        data = {
            'other': 'Hello, how are'
        }
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 500)

    @patch('document.views.PredictionService')
    def test_view_returns_json(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        try:
            response.json()
        except ValueError:
            self.fail('Response is not JSON.')

    @patch('document.views.PredictionService')
    def test_view_returns_prediction_field(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        try:
            response.json()['prediction']
        except KeyError:
            self.fail('Response has not prediction field.')

    @patch('document.views.PredictionService')
    def test_view_provides_prediction(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['prediction'], 'you')

    @patch('document.views.PredictionService')
    def test_view_predicts_with_desired_model(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        prediction_service_mock.instance.assert_called_once_with(self.test_user.settings.prediction_model)

    @patch('document.views.PredictionService')
    def test_view_predicts_with_desired_model_when_changed(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        self.test_user.settings.prediction_model = PredictionModels.GPT2
        self.test_user.save()
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        prediction_service_mock.instance.assert_called_once_with(PredictionModels.GPT2.value)

        self.test_user.settings.prediction_model = PredictionModels.BERT
        self.test_user.save()
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        prediction_service_mock.instance.assert_called_with(PredictionModels.BERT.value)

    @patch('document.views.PredictionService')
    def test_view_predicts_with_desired_text(self, prediction_service_mock):
        self.client.force_login(self.test_user)
        data = {
            'input': 'Hello, how are'
        }
        prediction_service_mock.instance.return_value.get_prediction.return_value = 'you'
        response = self.client.get(reverse('prediction'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        prediction_service_mock.instance().get_prediction.assert_called_once_with(data['input'])

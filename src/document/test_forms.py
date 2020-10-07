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

from django.test import TestCase

from document.forms import DocumentCreationForm, DocumentEditionForm


class DocumentCreationFormTest(TestCase):
    def test_form_contains_title(self):
        form = DocumentCreationForm()
        self.assertTrue('title' in form.base_fields)

    def test_form_contains_description(self):
        form = DocumentCreationForm()
        self.assertTrue('description' in form.base_fields)

    def test_form_title_is_mandatory(self):
        form = DocumentCreationForm({'description': 'test_description'})
        self.assertFalse(form.is_valid())

    def test_form_description_is_not_mandatory(self):
        form = DocumentCreationForm({'title': 'test_title'})
        self.assertTrue(form.is_valid())


class DocumentEditionFormTest(TestCase):
    def test_remember_body_label(self):
        form = DocumentEditionForm()
        self.assertTrue('body' in form.base_fields)

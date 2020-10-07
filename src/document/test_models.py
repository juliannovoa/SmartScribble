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
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from document.models import Document


class DocumentModelTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user')

    def test_title_max_length(self):
        title_max_length = Document.title.field.max_length
        self.assertEqual(title_max_length, 50)

        title = 'a' * 51
        document = Document.objects.create(title=title,
                                           description='test_description',
                                           body='test_body',
                                           user=self.test_user)
        with self.assertRaises(ValidationError):
            document.full_clean()

    def test_title_limit_max_length(self):
        title_max_length = Document.title.field.max_length
        self.assertEqual(title_max_length, 50)

        title = 'a' * 50
        document = Document.objects.create(title=title,
                                           description='test_description',
                                           body='test_body',
                                           user=self.test_user)
        try:
            document.full_clean()
        except ValidationError:
            self.fail('Document is not correct.')

    def test_description_max_length(self):
        description_max_length = Document.description.field.max_length
        self.assertEqual(description_max_length, 100)

        description = 'a' * 101
        document = Document.objects.create(title='test_title',
                                           description=description,
                                           body='test_body',
                                           user=self.test_user)
        with self.assertRaises(ValidationError):
            document.full_clean()

    def test_description_limit_max_length(self):
        description_max_length = Document.description.field.max_length
        self.assertEqual(description_max_length, 100)

        description = 'a' * 100
        document = Document.objects.create(title='test_title',
                                           description=description,
                                           body='test_body',
                                           user=self.test_user)
        try:
            document.full_clean()
        except ValidationError:
            self.fail('Document is not correct.')

    def test_title_is_mandatory(self):

        document = Document.objects.create(description='test_description',
                                           body='test_body',
                                           user=self.test_user)
        with self.assertRaises(ValidationError):
            document.full_clean()

    def test_description_is_not_mandatory(self):

        document = Document.objects.create(title='test_title',
                                           body='test_body',
                                           user=self.test_user)
        try:
            document.full_clean()
        except ValidationError:
            self.fail('Document is not correct.')

    def test_body_is_not_mandatory(self):

        document = Document.objects.create(title='test_title',
                                           description='test_description',
                                           user=self.test_user)
        try:
            document.full_clean()
        except ValidationError:
            self.fail('Document is not correct.')

    def test_user_is_mandatory(self):
        with self.assertRaises(IntegrityError):
            Document.objects.create(title='test_title',
                                    description='test_description',
                                    body='test_body')

    def test_document_deletion_after_user_deletion(self):

        document = Document.objects.create(title='test_title',
                                           description='test_description',
                                           body='test_body',
                                           user=self.test_user)
        try:
            document.full_clean()
        except ValidationError:
            self.fail('Document is not correct.')

        document.save()
        document_pk = document.pk
        self.assertEqual(Document.objects.get(pk=document_pk), document)
        self.test_user.delete()
        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(pk=document_pk)

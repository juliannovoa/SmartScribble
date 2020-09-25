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

from register.models import PredictionModels


class UserCreationTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test_user')

    def test_settings_label(self):
        user = User.objects.get(username="test_user")
        field_settings_label = user._meta.get_field('settings').name
        self.assertEqual(field_settings_label, 'settings')

    def test_prediction_model_label(self):
        user = User.objects.get(username="test_user")
        field_prediction_model = user.settings._meta.get_field('prediction_model')
        field_prediction_model_label = field_prediction_model.verbose_name
        self.assertEqual(field_prediction_model_label, 'prediction model')

    def test_prediction_model_length(self):
        user = User.objects.get(username="test_user")
        field_prediction_model = user.settings._meta.get_field('prediction_model')
        max_length = field_prediction_model.max_length
        self.assertEqual(max_length, 6)

    def test_has_prediction_model(self):
        user = User.objects.get(username="test_user")
        self.assertIsNotNone(user.settings)
        self.assertIsNotNone(user.settings.prediction_model)


class PredictionModelsTest(TestCase):
    def test_is_prediction_models_not_empty(self):
        self.assertGreater(len(PredictionModels), 0)

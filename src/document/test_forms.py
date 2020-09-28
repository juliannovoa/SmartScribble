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

# from django.test import TestCase
#
#
# class DocumentCreationFormTest(TestCase):
#     def test_form_contains_email(self):
#         form = RegisterForm()
#         self.assertTrue('email' in form.base_fields)
#
#
# class DocumentEditionFormTest(TestCase):
#     def test_remember_field_label(self):
#         form = LoginForm()
#         self.assertTrue('remember_me' in form.fields)
#         field_label = form.fields['remember_me'].label
#         self.assertEqual(field_label, 'Remember me')
#
#     def test_remember_field_not_required(self):
#         form = LoginForm()
#         self.assertTrue('remember_me' in form.fields)
#         self.assertFalse(form.fields['remember_me'].required)
#
#
# class PredictionModelFormTest(TestCase):
#     def test_selected_prediction_model_label(self):
#         form = PredictionModelForm()
#         self.assertTrue('selected_prediction_model' in form.fields)
#         field_label = form.fields['selected_prediction_model'].label
#         self.assertTrue(field_label == 'selected prediction model' or field_label is None)
#
#     def test_prediction_models_options(self):
#         form = PredictionModelForm()
#         self.assertTrue('selected_prediction_model' in form.fields)
#         choices = form.fields['selected_prediction_model']._choices
#         self.assertIsNotNone(choices)
#         for model in PredictionModels:
#             self.assertTrue((model.name, model.value) in choices)
#         self.assertEqual(len(choices), len(PredictionModels))
#
#     def test_form_created_correct_with_model_names(self):
#         for model in PredictionModels:
#             data = {'selected_prediction_model': model.name}
#             self.assertTrue(PredictionModelForm(data).is_valid())
#
#     def test_form_detects_incorrect_input(self):
#         data = {'selected_prediction_model': "invalid_name"}
#         self.assertFalse(PredictionModelForm(data).is_valid())

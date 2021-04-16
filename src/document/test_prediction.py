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
import sys
from unittest.mock import patch, Mock

from django.test import TestCase
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AlbertTokenizer, AlbertForMaskedLM

from document.prediction import PredictionModel
from register.models import PredictionModels


class PredictionServiceTest(TestCase):

    # noinspection PyUnresolvedReferences
    def setUp(self):
        del sys.modules['document.prediction']
        from document.prediction import PredictionService

    def test_nonexistent_prediction_model(self):
        from document.prediction import PredictionService
        with self.assertRaises(ValueError):
            PredictionService.instance('nonexistent')

    @patch('document.prediction.PredictionModel')
    def test_prediction_service_instance_creates_prediction_model_if_not_exists(self, prediction_model_mock):
        from document.prediction import PredictionService
        PredictionService.instance(PredictionModels.GPT2.name)
        prediction_model_mock.assert_called_once()

    @patch('document.prediction.PredictionModel')
    def test_prediction_service_instance_creates_prediction_model_only_once(self, prediction_model_mock):
        from document.prediction import PredictionService
        model1 = PredictionService.instance(PredictionModels.GPT2.name)
        model2 = PredictionService.instance(PredictionModels.GPT2.name)
        prediction_model_mock.assert_called_once()
        self.assertEqual(model1, model2)


class PredictionModelTest(TestCase):
    def setUp(self):
        self.tokenizer = Mock()
        self.model = Mock()
        self.pretrained_model = 'pretrained_model'
        self.need_mask = True

    def test_prediction_model_creation_loads_tokenizer(self):
        PredictionModel(self.tokenizer, self.model, self.pretrained_model, self.need_mask)
        self.tokenizer.from_pretrained.assert_called_once_with(self.pretrained_model)

    def test_prediction_model_creation_loads_model(self):
        PredictionModel(self.tokenizer, self.model, self.pretrained_model, self.need_mask)
        self.model.from_pretrained.assert_called_once_with(self.pretrained_model)

    def test_prediction_model_is_in_evaluation_mode(self):
        prediction_model = PredictionModel(self.tokenizer, self.model, self.pretrained_model, self.need_mask)
        prediction_model._model.eval.assert_called_once()

    def test_prediction_model_need_mask_is_set(self):
        prediction_model = PredictionModel(self.tokenizer, self.model, self.pretrained_model, self.need_mask)
        self.assertEqual(prediction_model._need_mask, self.need_mask)

    def test_get_prediction_no_mask_model(self):
        prediction_model = PredictionModel(GPT2Tokenizer, GPT2LMHeadModel, 'gpt2', False)
        text = 'How are '
        prediction = prediction_model.get_prediction(text)
        self.assertEqual(prediction, 'you')

    def test_get_prediction_mask_model_with_end_space(self):
        prediction_model = PredictionModel(AlbertTokenizer, AlbertForMaskedLM, 'albert-base-v2', True)
        text = 'How are '
        prediction = prediction_model.get_prediction(text)
        self.assertEqual(prediction, '')

    @patch('document.prediction.PredictionModel._tokenize')
    @patch('document.prediction.PredictionModel._predict')
    def test_prediction_output_no_mask(self, pred_mock, tok_mock):
        pred_mock.return_value = 'you'
        prediction_model = PredictionModel(Mock(), Mock(), Mock(), False)
        response = prediction_model.get_prediction('How are')
        self.assertEqual(response, '')

    @patch('document.prediction.PredictionModel._tokenize')
    @patch('document.prediction.PredictionModel._predict')
    def test_prediction_output_no_mask_end_space(self, pred_mock, tok_mock):
        pred_mock.return_value = 'you'
        prediction_model = PredictionModel(Mock(), Mock(), Mock(), False)
        response = prediction_model.get_prediction('How are ')
        self.assertEqual(response, '')

    @patch('document.prediction.PredictionModel._tokenize')
    @patch('document.prediction.PredictionModel._predict')
    def test_prediction_output_no_mask_half_word(self, pred_mock, tok_mock):
        pred_mock.return_value = 'you'
        prediction_model = PredictionModel(Mock(), Mock(), Mock(), False)
        response = prediction_model.get_prediction('How are y')
        self.assertEqual(response, '')

    @patch('document.prediction.PredictionModel._tokenize')
    @patch('document.prediction.PredictionModel._predict')
    def test_prediction_output_with_mask(self, pred_mock, tok_mock):
        pred_mock.return_value = 'you'
        prediction_model = PredictionModel(Mock(), Mock(), Mock(), True)
        response = prediction_model.get_prediction('How are')
        self.assertEqual(response, '')

    @patch('document.prediction.PredictionModel._tokenize')
    @patch('document.prediction.PredictionModel._predict')
    def test_prediction_output_with_mask_end_space(self, pred_mock, tok_mock):
        pred_mock.return_value = 'you'
        prediction_model = PredictionModel(Mock(), Mock(), Mock(), True)
        response = prediction_model.get_prediction('How are ')
        self.assertEqual(response, '')

    @patch('document.prediction.PredictionModel._tokenize')
    @patch('document.prediction.PredictionModel._predict')
    def test_prediction_output_with_mask_half_word(self, pred_mock, tok_mock):
        pred_mock.return_value = 'you'
        prediction_model = PredictionModel(Mock(), Mock(), Mock(), True)
        response = prediction_model.get_prediction('How are y')
        self.assertEqual(response, '')

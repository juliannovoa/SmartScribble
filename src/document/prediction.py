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

import torch
from filelock import FileLock
from transformers import AlbertTokenizer, AlbertForMaskedLM, GPT2Tokenizer, GPT2LMHeadModel, BertTokenizer, \
    BertForMaskedLM, BatchEncoding
from transformers.utils import logging

from register.models import PredictionModels

LOCK_TIMEOUT = 10
LOCK_FILE = 'prediction.lock'


class PredictionModel:
    def __init__(self, tokenizer, head_model, pretrained: str, needs_mask: bool):
        logging.set_verbosity_warning()
        self._tokenizer = tokenizer.from_pretrained(pretrained)
        self._model = head_model.from_pretrained(pretrained)
        self._need_mask = needs_mask
        # Set the model in evaluation mode to deactivate the DropOut modules
        self._model.eval()

    def _tokenize(self, text: str) -> BatchEncoding:
        if self._need_mask:
            text = text.rsplit(' ', 1)[0]
            text += f' {self._tokenizer.mask_token}.'
        else:
            text = text.rstrip()
        return self._tokenizer(text, return_tensors='pt')

    def _predict(self, prediction_inputs: BatchEncoding) -> str:

        with torch.no_grad():
            outputs = self._model(**prediction_inputs)
            predictions = outputs[0]

        predicted_index = torch.argmax(predictions[0, -1]).item()

        if self._need_mask:
            predicted_token = self._tokenizer.decode([predicted_index])
        else:
            predicted_sentence = self._tokenizer.decode(
                prediction_inputs.input_ids.tolist()[0] + [predicted_index])
            predicted_token = predicted_sentence.split()[-1]

        return predicted_token

    @staticmethod
    def _get_last_word(text: str) -> str:
        if not text:
            return ''
        elif text[-1] == ' ':
            return ' '
        words = text.split()
        return words[-1] if words[-1] != '&nbsp;' else ' '

    def get_prediction(self, text: str) -> str:
        prediction_inputs = self._tokenize(text)
        prediction = self._predict(prediction_inputs)
        last_word = PredictionModel._get_last_word(text)
        if prediction.startswith(last_word):
            return prediction[len(last_word):]
        elif last_word == ' ':
            return prediction
        elif self._need_mask:
            return ''
        else:
            return "&nbsp;" + prediction


class PredictionService:
    __instances = {}
    __params = {
        PredictionModels.GPT2.name: (GPT2Tokenizer, GPT2LMHeadModel, 'gpt2-medium', False),
        PredictionModels.DGPT2.name: (GPT2Tokenizer, GPT2LMHeadModel, 'distilgpt2', False),
        PredictionModels.BERT.name: (BertTokenizer, BertForMaskedLM, 'bert-base-cased', True),
        PredictionModels.ALBERT.name: (AlbertTokenizer, AlbertForMaskedLM, 'albert-xxlarge-v2', True),
    }

    @staticmethod
    def instance(prediction_model: str) -> PredictionModel:
        if prediction_model not in PredictionService.__params:
            raise ValueError()
        if prediction_model not in PredictionService.__instances:
            with FileLock(LOCK_FILE).acquire(timeout=LOCK_TIMEOUT):
                if prediction_model not in PredictionService.__instances:
                    PredictionService.__instances[prediction_model] = PredictionService._create(prediction_model)
        return PredictionService.__instances[prediction_model]

    @staticmethod
    def _create(prediction_model):
        tokenizer, head_model, pretrained, needs_mask = PredictionService.__params[prediction_model]
        return PredictionModel(tokenizer, head_model, pretrained, needs_mask)

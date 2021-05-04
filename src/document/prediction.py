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
from transformers import AlbertTokenizer, AlbertForMaskedLM, GPT2Tokenizer, GPT2LMHeadModel, BertTokenizer, \
    BertForMaskedLM, BatchEncoding, pipeline
from transformers.utils import logging

from register.models import PredictionModels

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

    def _get_predicted_item_position(self, prediction_inputs: BatchEncoding) -> int:
        if not self._need_mask:
            return -1
        return torch.nonzero(prediction_inputs['input_ids'][0] == self._tokenizer.mask_token_id,
                             as_tuple=False).item()

    def _predict(self, text: str) -> str:
        prediction_inputs = self._tokenize(text)
        if self._need_mask:
            return self._predict_with_mask(prediction_inputs)
        else:
            return self._predict_no_mask(prediction_inputs)

    def _predict_no_mask(self, prediction_inputs: BatchEncoding) -> str:
        with torch.no_grad():
            outputs = self._model(**prediction_inputs)
            predictions = outputs[0]
        predicted_token_index = torch.argmax(
            predictions[0, self._get_predicted_item_position(prediction_inputs)]).item()
        predicted_sentence = self._tokenizer.decode(
            prediction_inputs.input_ids.tolist()[0] + [predicted_token_index])
        return predicted_sentence

    def _predict_with_mask(self, prediction_inputs: BatchEncoding) -> str:
        with torch.no_grad():
            outputs = self._model(**prediction_inputs)
            predictions = outputs[0]
        predicted_token_index = torch.argmax(
            predictions[0, self._get_predicted_item_position(prediction_inputs)]).item()
        predicted_sentence = self._tokenizer.decode(
            prediction_inputs.input_ids.tolist()[0] + [predicted_token_index], skip_special_tokens=True)
        return ''.join(predicted_sentence.rsplit('.', 1))

    @staticmethod
    def _get_last_word(text: str) -> str:
        if not text:
            return ''
        elif text[-1] == ' ':
            return ' '
        words = text.split()
        return words[-1] if words[-1] != '&nbsp;' else ' '

    def get_prediction(self, text: str) -> str:
        predicted_sentence = self._predict(text)

        if not predicted_sentence.lower().startswith(text.lower()):
            return ''

        prediction = predicted_sentence[len(text):]

        if prediction.startswith(' '):
            return "&nbsp;" + prediction.lstrip()
        else:
            return prediction

    def get_full_prediction(self, text: str) -> str:
        generator = pipeline('text-generation', model=self._model, tokenizer=self._tokenizer)
        prediction = generator(text, num_return_sequences=1, no_repeat_ngram_size=2, max_length=len(text)+20,
                               early_stopping=True, num_beams=5)[0]['generated_text']
        last_point = prediction.rfind('.')
        if last_point != -1:
            output = prediction[len(text):last_point+1]
        else:
            output = prediction[len(text):]
        if output.startswith(' '):
            return "&nbsp;" + output.lstrip()
        else:
            return output


class PredictionService:
    __instances = {}
    __params = {
        PredictionModels.GPT2.name: (GPT2Tokenizer, GPT2LMHeadModel, 'gpt2-medium', False),
        PredictionModels.DGPT2.name: (GPT2Tokenizer, GPT2LMHeadModel, 'distilgpt2', False),
        PredictionModels.BERT.name: (BertTokenizer, BertForMaskedLM, 'bert-base-cased', True),
        PredictionModels.ALBERT.name: (AlbertTokenizer, AlbertForMaskedLM, 'albert-large-v2', True),
    }

    @staticmethod
    def instance(prediction_model: str) -> PredictionModel:
        if prediction_model not in PredictionService.__params:
            raise ValueError()
        if prediction_model not in PredictionService.__instances:
            if prediction_model not in PredictionService.__instances:
                PredictionService.__instances[prediction_model] = PredictionService._create(prediction_model)
        return PredictionService.__instances[prediction_model]

    @staticmethod
    def _create(prediction_model):
        tokenizer, head_model, pretrained, needs_mask = PredictionService.__params[prediction_model]
        return PredictionModel(tokenizer, head_model, pretrained, needs_mask)

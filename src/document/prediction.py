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
from transformers import AlbertTokenizer, AlbertModel, GPT2Tokenizer, GPT2LMHeadModel, BertTokenizer, \
    BertLMHeadModel

from register.models import PredictionModels

LOCK_TIMEOUT = 10
LOCK_FILE = "prediction.lock"


class PredictionService:
    __instances = {}
    __params = {
        PredictionModels.GPT2.name: (GPT2Tokenizer, GPT2LMHeadModel, 'gpt2-large'),
        PredictionModels.DGPT2.name: (GPT2Tokenizer, GPT2LMHeadModel, 'distilgpt2'),
        PredictionModels.BERT.name: (BertTokenizer, BertLMHeadModel, 'bert-base-cased'),
        PredictionModels.ALBERT.name: (AlbertTokenizer, AlbertModel, 'albert-xxlarge-v2'),
    }

    @staticmethod
    def instance(prediction_model):
        if prediction_model not in PredictionService.__params:
            raise ValueError()
        if prediction_model not in PredictionService.__instances:
            with FileLock(LOCK_FILE).acquire(timeout=LOCK_TIMEOUT):
                if prediction_model not in PredictionService.__instances:
                    PredictionService.__instances[prediction_model] = PredictionService.create(prediction_model)
        return PredictionService.__instances[prediction_model]

    @staticmethod
    def create(prediction_model):
        tokenizer, head_model, pretrained = PredictionService.__params[prediction_model]
        return PredictionModel(tokenizer, head_model, pretrained)


class PredictionModel:

    def __init__(self, tokenizer, head_model, pretrained):
        # Load pre-trained model tokenizer (vocabulary)
        self.tokenizer = tokenizer.from_pretrained(pretrained)
        # Load pre-trained model (weights)
        self.model = head_model.from_pretrained(pretrained)
        # Set the model in evaluation mode to deactivate the DropOut modules
        self.model.eval()

    def _predict(self, text):

        # Index input
        indexed_tokens = self.tokenizer.encode(text)

        # Convert indexed tokens in a PyTorch tensor
        tokens_tensor = torch.tensor([indexed_tokens])

        # Predict all tokens
        with torch.no_grad():
            outputs = self.model(tokens_tensor)
            predictions = outputs[0]

        # Get the predicted next sub-word
        predicted_index = torch.argmax(predictions[0, -1, :]).item()
        predicted_sentence = self.tokenizer.decode(indexed_tokens + [predicted_index])
        print(predicted_sentence)
        return predicted_sentence.split()[-1]

    @staticmethod
    def _get_last_word(text):
        if text[-1] == " " or text[-1] == "&nbsp":
            return " "
        return text.split()[-1]

    def get_prediction(self, text):
        prediction = self._predict(text)
        last_word = PredictionModel._get_last_word(text)
        if prediction.startswith(last_word):
            return prediction[len(last_word):]
        elif last_word == " ":
            return prediction
        else:
            return "&nbsp;" + prediction

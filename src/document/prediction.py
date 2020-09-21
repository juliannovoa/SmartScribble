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
from transformers import AlbertTokenizer, AlbertModel, GPT2Tokenizer, GPT2LMHeadModel, BertTokenizer, BertModel

from register.models import PredictionModels

LOCK_TIMEOUT = 10
LOCK_FILE = "prediction.lock"


class PredictionService:
    __instances = {}
    __params = {
        PredictionModels.GPT2.name: (GPT2Tokenizer, GPT2LMHeadModel, 'gpt2-xl'),
        PredictionModels.BERT.name: (BertTokenizer, BertModel, 'bert-base-uncased'),
        PredictionModels.ALBERT.name: (AlbertTokenizer, AlbertModel, 'albert-xxlarge-v2'),
    }

    @staticmethod
    def instance(prediction_model):
        print(prediction_model)
        if prediction_model not in PredictionService.__params:
            raise ValueError()
        if prediction_model not in PredictionService.__instances:
            with FileLock(LOCK_FILE).acquire(timeout=LOCK_TIMEOUT):
                if prediction_model not in PredictionService.__instances:
                    print("Empieza Carga modelo")
                    PredictionService.__instances[prediction_model] = PredictionService.create(prediction_model)
                    print("Fin Carga modelo")
        return PredictionService.__instances[prediction_model]

    @staticmethod
    def create(prediction_model):
        print("Empieza crear modelo")
        tokenizer, head_model, pretrained = PredictionService.__params[prediction_model]
        print("Fin crear modelo")
        return PredictionModel(tokenizer, head_model, pretrained)


class PredictionModel:

    def __init__(self, tokenizer, head_model, pretrained):
        # Load pre-trained model tokenizer (vocabulary)
        print("Crear tokenicer en instancia")
        self.tokenizer = tokenizer.from_pretrained(pretrained)
        print("Crear tokenicer en instancia 2")
        # Load pre-trained model (weights)
        print("Carga modelo en instancia")
        self.model = head_model.from_pretrained(pretrained)
        print("Carga modelo en instancia 2")
        # Set the model in evaluation mode to deactivate the DropOut modules
        self.model.eval()
        print("Instancia creada")

    def _predict(self, text):
        indexed_tokens = self.tokenizer.encode(text)

        # Convert indexed tokens in a PyTorch tensor
        tokens_tensor = torch.tensor([indexed_tokens])

        # Predict all tokens
        with torch.no_grad():
            outputs = self.model(tokens_tensor)
            predictions = outputs[0]

        # Get the predicted next sub-word
        predicted_index = torch.argmax(predictions[0, -1, :]).item()
        predicted_text = self.tokenizer.decode(indexed_tokens + [predicted_index])
        return predicted_text.split()[-1]

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

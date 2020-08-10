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


# Create your views here.
import json
import re

import torch
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel

from document.models import Document
from .forms import DocumentEditionForm


@login_required
def remove_document_view(request):
    doc_id = request.POST['docId']
    doc = get_object_or_404(Document, pk=doc_id)
    if doc.user != request.user:
        raise PermissionDenied
    doc.delete()
    return redirect('profile')


@login_required
def edit_document_view(request):
    if request.method == "GET":
        doc_id = request.GET['docId']
        doc = get_object_or_404(Document, pk=doc_id)
        if doc.user != request.user:
            raise PermissionDenied
    if request.method == "POST":
        doc_id = request.GET['docId']
        doc = get_object_or_404(Document, pk=doc_id)
        if doc.user != request.user:
            raise PermissionDenied
        form = DocumentEditionForm(request.POST, instance=doc)
        doc = form.save()
    return render(request, "document/textEditor.html",
                  {'form': DocumentEditionForm(initial={'body': doc.body})})


class PredictionService:
    __instance = None

    def __init__(self):
        if PredictionService.__instance is not None:
            raise Exception("PredictionService is a singleton, use instance()")
        # Load pre-trained model tokenizer (vocabulary)
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        # Load pre-trained model (weights)
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        # Set the model in evaluation mode to deactivate the DropOut modules
        self.model.eval()

    @staticmethod
    def instance():
        if PredictionService.__instance is None:
            PredictionService.__instance = PredictionService()
        return PredictionService.__instance

    def _clean_text(self, text):
        # usar library de html
        cleaner = re.compile('<.*?>')
        return re.sub(cleaner, '', text)

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

    def _get_last_word(self, text):
        if text[-1] == " " or text[-1] == "&nbsp":
            return " "
        return text.split()[-1]

    def _get_output(self, prediction, last_word):
        if prediction.startswith(last_word):
            return prediction[len(last_word):]
        elif last_word == " ":
            return prediction
        else:
            return "&nbsp;" + prediction

    def get_prediction(self, text):
        last_word = self._get_last_word(text)
        prediction = self._predict(text)
        return self._get_output(prediction, last_word)


@login_required
def predict(request):
    if request.method == 'GET' and request.is_ajax():
        # Encode a text inputs
        text = request.GET['input']
        prediction = PredictionService.instance().get_prediction(text)
        return HttpResponse(json.dumps({'prediction': prediction}))

    return HttpResponse()
    # predictions = ['hola', 'adios', 'Casa', 'perro', 'gato']
    # if request.method == 'GET' and request.is_ajax():
    #     word = predictions[random.randint(0, 4)]
    #     return HttpResponse(json.dumps({'prediction': word}))
    # return HttpResponse()

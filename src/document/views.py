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


from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentEditionForm, ChangeNameDocumentForm, ChangeDescriptionDocumentForm
from .models import Document
from .prediction import PredictionService
from register.models import PredictionModels


@login_required
def remove_document_view(request):
    """

    Remove a document

    Args:
        request: HTTP request

    Returns: HTTP response

    """
    if request.method == 'POST':
        doc_id = request.POST['doc_id']
        doc = get_object_or_404(Document, pk=doc_id)
        if doc.user != request.user:
            raise PermissionDenied
        doc.delete()
        return redirect('profile')
    else:
        return HttpResponseServerError('Wrong request.')


@login_required
def edit_document_view(request):
    """

    Edit a document

    Args:
        request: HTTP request

    Returns: HTTP response

    """
    if request.method == 'GET':
        doc_id = request.GET['id']
    elif request.method == 'POST':
        doc_id = request.POST['id']
    else:
        return HttpResponseServerError('Wrong request')

    doc = get_object_or_404(Document, pk=doc_id)
    if doc.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        if 'title' in request.POST:
            form = ChangeNameDocumentForm(request.POST, instance=doc)
            doc = form.save()
        elif 'description' in request.POST:
            form = ChangeDescriptionDocumentForm(request.POST, instance=doc)
            doc = form.save()
        else:
            return HttpResponseServerError('Error')
    data = {'formEdit': DocumentEditionForm(initial={'body': doc.body, 'id': doc_id}),
            'formName': ChangeNameDocumentForm(initial={'id': doc_id}),
            'formDescription': ChangeDescriptionDocumentForm(initial={'id': doc_id}),
            'title': doc.title,
            'description': doc.description, }

    return render(request, 'document/textEditor.html', data)


@login_required
def save_document_view(request):
    """

    Save a document

    Args:
        request: HTTP request

    Returns: HTTP response

    """
    if request.method == 'POST':
        doc_id = request.POST['id']
        doc = get_object_or_404(Document, pk=doc_id)
        form = DocumentEditionForm(request.POST, instance=doc)
        doc = form.save()
        return HttpResponse('Saved')
    else:
        return HttpResponseServerError('Error saving')


@login_required
def predict_view(request):
    """

    Get a prediction

    Args:
        request: HTTP request

    Returns: HTTP response

    """
    INPUT_KEY = 'input'
    if request.method == 'GET' and request.is_ajax() and INPUT_KEY in request.GET:
        # Encode a text inputs
        text = request.GET[INPUT_KEY]
        prediction = PredictionService.instance(request.user.settings.prediction_model).get_prediction(text)
        return JsonResponse({'prediction': prediction, 'input_text': text})
    return HttpResponseServerError('Empty request.')


@login_required
def full_predict_view(request):
    """

    Get a long prediction

    Args:
        request: HTTP request

    Returns: HTTP response

    """
    INPUT_KEY = 'input'
    if request.method == 'GET' and request.is_ajax() and INPUT_KEY in request.GET:
        # Encode a text inputs
        text = request.GET[INPUT_KEY]
        if request.user.settings.prediction_model == PredictionModels.GPT2.name:
            predictor = PredictionModels.GPT2.name
        else:
            predictor = PredictionModels.DGPT2.name
        prediction = PredictionService.instance(predictor).get_full_prediction(text)
        return JsonResponse({'prediction': prediction, 'input_text': text})
    return HttpResponseServerError('Empty request.')

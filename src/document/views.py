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

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentEditionForm
from .models import Document
from .prediction import PredictionService


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


@login_required
def predict(request):
    if request.method == 'GET' and request.is_ajax():
        # Encode a text inputs
        text = request.GET['input']
        prediction = PredictionService.instance().get_prediction(text)
        return HttpResponse(json.dumps({'prediction': prediction}))

    return HttpResponse()

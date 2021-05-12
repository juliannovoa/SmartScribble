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

from ckeditor.fields import RichTextFormField
from django import forms

from .models import Document


class DocumentCreationForm(forms.ModelForm):
    """ Formulary designed to create instances of documents """
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your title'}))
    description = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Description (optional)'}))

    class Meta:
        model = Document
        fields = [
            'title',
            'description',
        ]


class DocumentEditionForm(forms.ModelForm):
    """ Formulary designed to edit instances of documents """
    body = RichTextFormField(label="", required=False)
    id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Document
        fields = [
            'body',
            'id'
        ]


class ChangeNameDocumentForm(forms.ModelForm):
    """ Formulary designed to change the name of a document """
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New title'}))
    id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Document
        fields = [
            'title',
            'id',
        ]


class ChangeDescriptionDocumentForm(forms.ModelForm):
    """ Formulary designed to change the description of a document """
    description = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'New description'}))
    id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Document
        fields = [
            'description',
            'id',
        ]
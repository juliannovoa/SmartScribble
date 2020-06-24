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
from django.shortcuts import render

from document.forms import DocumentCreationForm
from document.models import Document


# Create your views here.
def home_view(request):
    return render(request, 'pages/home.html')


@login_required
def profile_view(request):
    docs = Document.objects.filter(user__exact=request.user)
    if request.method == "POST":
        form = DocumentCreationForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()

    return render(request, "pages/profile.html", {'form': DocumentCreationForm(), 'docs': docs})

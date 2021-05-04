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
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_control

from document.forms import DocumentCreationForm
from document.models import Document


# Create your views here.

@login_required
def profile_view(request):
    docs = Document.objects.filter(user__exact=request.user)
    if request.method == "POST":
        form = DocumentCreationForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect(('{}?id='+str(doc.id)).format(reverse('edit')))
        return HttpResponseServerError('Error. Document cannot be created.')
    return render(request, "pages/profile.html", {'form': DocumentCreationForm(), 'docs': docs})


@login_required
def change_data_view(request):
    if request.method == "POST":
        usr = get_object_or_404(User, pk=request.user.pk)
        try:
            usr.delete()
        except Exception:
            return HttpResponseServerError('Error. User was not removed.')
        return redirect('initial')
    return render(request, "pages/changedata.html")

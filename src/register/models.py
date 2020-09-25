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

# Create your models here.


from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PredictionModels(models.TextChoices):
    GPT2 = 'gpt-2'
    BERT = 'bert'
    ALBERT = 'albert'


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prediction_model = models.CharField(max_length=6,
                                        choices=PredictionModels.choices,
                                        default=PredictionModels.GPT2.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.settings.save()

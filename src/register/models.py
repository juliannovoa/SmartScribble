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
    DGPT2 = 'distil-gpt2'


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prediction_model = models.CharField(max_length=15,
                                        choices=PredictionModels.choices,
                                        default=PredictionModels.GPT2.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.settings.save()


descriptions = {
    'gpt-2': 'Generative Pre-trained Transformer 2 (GPT2) is a language model developed by OpenAI. This version '
             'includes 82 million parameters.',
    'bert': 'Bidirectional Encoder Representations from Transformers (BERT) is a language model developed by Google. '
            'This version includes 109 million parameters.',
    'albert': 'A Lite BERT (ALBERT) is a language model developed by Google from BERT to improve its performance. '
              'This version includes 58 million parameters.',
    'distil-gpt2': 'Distilled version of GPT2. It includes 82 million parameters. It achieves shorter inference times '
                   'without significant loss of prediction quality.'
}

more_info = {
    'gpt-2': 'https://openai.com/blog/better-language-models/',
    'bert': 'https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html',
    'albert': 'https://ai.googleblog.com/2019/12/albert-lite-bert-for-self-supervised.html',
    'distil-gpt2': 'https://huggingface.co/distilgpt2'
}

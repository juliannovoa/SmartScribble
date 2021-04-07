import logging
import os
import sys

from django.apps import AppConfig


class DocumentConfig(AppConfig):
    name = 'document'

    def ready(self):
        from register.models import PredictionModels
        from .prediction import PredictionService
        print(os.environ)
        if 'test' not in sys.argv:
            print('not testing')
            logger = logging.getLogger("DocumentConfig")
            for model in PredictionModels:
                logger.info(f"Preloading model {model.name}")
                PredictionService.instance(model.name)

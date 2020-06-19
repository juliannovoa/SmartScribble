from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

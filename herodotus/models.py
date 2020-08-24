from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Content(models.Model):
    TYPE_CHOICES = {
        ('article', 'article'),
        ('note', 'note'),
    }
    content_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    url = models.CharField(max_length=500, null=True, blank=True)
    author = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
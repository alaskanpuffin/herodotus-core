from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os
import meilisearch

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
    richtext = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Content)
def update_search_index(sender, **kwargs):
    instance = kwargs.get('instance')
    client = meilisearch.Client(os.environ['MEILI_SEARCH_URL'], os.environ['MEILI_SEARCH_MASTER_KEY'])
    index = client.get_or_create_index('article', {'primaryKey': 'article_id'})
    index.add_documents([{'article_id': instance.id, 'content': instance.content, 'title': instance.title, 'author': instance.author}])

@receiver(post_delete, sender=Content)
def delete_search_index(sender, **kwargs):
    instance = kwargs.get('instance')
    client = meilisearch.Client(os.environ['MEILI_SEARCH_URL'], os.environ['MEILI_SEARCH_MASTER_KEY'])
    index = client.get_or_create_index('article', {'primaryKey': 'article_id'})
    index.delete_document(instance.id)
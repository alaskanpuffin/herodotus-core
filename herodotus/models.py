from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
import os
from django.db import transaction
import meilisearch

def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner

class User(AbstractUser):
    pass


class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=10, blank=True, null=True)


class Feed(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    last_updated = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)


class FeedHistory(models.Model):
    url = models.CharField(max_length=500)
    feed = models.ForeignKey(
        'Feed',
        on_delete=models.CASCADE,
    )


class Content(models.Model):
    TYPE_CHOICES = {
        ('article', 'article'),
        ('note', 'note'),
    }
    content_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    url = models.CharField(max_length=500, null=True, blank=True)
    author = models.CharField(max_length=300, null=True, blank=True)
    publisher = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    richtext = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Content)
def update_search_index(sender, **kwargs):
    instance = kwargs.get('instance')
    tags = []
    for tag in instance.tags.all():
        tags.append(tag.title)
    client = meilisearch.Client(
        os.environ['MEILI_SEARCH_URL'], os.environ['MEILI_SEARCH_MASTER_KEY'])
    index = client.get_or_create_index('article', {'primaryKey': 'article_id'})
    index.add_documents([{'article_id': instance.id, 'content': instance.content, 'title': instance.title,
                          'author': instance.author, 'publisher': instance.publisher, 'date': str(instance.date), 'tags': tags}])
    client.get_index('article').update_attributes_for_faceting([
        'tags',
    ])


@receiver(post_delete, sender=Content)
def delete_search_index(sender, **kwargs):
    instance = kwargs.get('instance')
    client = meilisearch.Client(
        os.environ['MEILI_SEARCH_URL'], os.environ['MEILI_SEARCH_MASTER_KEY'])
    index = client.get_or_create_index('article', {'primaryKey': 'article_id'})
    index.delete_document(instance.id)
    client.get_index('article').update_attributes_for_faceting([
        'tags',
    ])

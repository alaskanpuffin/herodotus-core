from django.core.management.base import BaseCommand, CommandError
from herodotus.models import Content
import meilisearch
import os


class Command(BaseCommand):
    help = 'Uploads all articles to MeiliSearch server for indexing.'

    def handle(self, *args, **options):
        client = meilisearch.Client(os.environ['MEILI_SEARCH_URL'], os.environ['MEILI_SEARCH_MASTER_KEY'])
        index = client.get_or_create_index('article', {'primaryKey': 'article_id'})
        documents = []

        contentQuerySet = Content.objects.all()

        for article in contentQuerySet:
            documents.append({'article_id': article.id, 'content': article.content, 'title': article.title, 'author': article.author})

        index.delete_all_documents()
        index.add_documents(documents)

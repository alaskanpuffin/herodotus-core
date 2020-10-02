from .models import Content, User, Feed
from .serializers import ContentSerializer, ScrapedArticleSerializer, UserSerializer, FeedSerializer
from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from newspaper import Article
from rest_framework import permissions
from .pagination import ContentPagination
import os
from django.db.models import Case, When
import meilisearch
from django.conf import settings
from django.http import HttpResponse
import json


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.order_by('-id')
    serializer_class = ContentSerializer
    pagination_class = ContentPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.order_by('-id')
    serializer_class = FeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SearchContent(generics.ListCreateAPIView):
    pagination_class = ContentPagination
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def list(self, request):
        search_ids = []

        search = request.GET.get('q')

        client = meilisearch.Client(
            os.environ['MEILI_SEARCH_URL'], os.environ['MEILI_SEARCH_MASTER_KEY'])
        index = client.get_or_create_index(
            'article', {'primaryKey': 'article_id'})

        results = index.search(search)

        for result in results['hits']:
            search_ids.append(result['article_id'])

        preserved = Case(*[When(pk=pk, then=pos)
                           for pos, pk in enumerate(search_ids)])
        queryset = self.get_queryset().filter(id__in=search_ids).order_by(preserved)

        paginator = ContentPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = ContentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ScrapeArticle(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        url = request.GET.get('url')
        article = Article(url)
        article.download()
        article.parse()

        if not article.authors == []:
            article.authors = article.authors[0]
        else:
            article.authors = ""

        data = {"url": url, "title": article.title, "content": article.text,
                "author": article.authors, "date": article.publish_date}

        results = ScrapedArticleSerializer(data, many=False).data
        return Response(results)


class IndexArticles(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        client = meilisearch.Client(
            os.environ['MEILI_SEARCH_URL'], os.environ['MEILI_SEARCH_MASTER_KEY'])
        index = client.get_or_create_index(
            'article', {'primaryKey': 'article_id'})
        documents = []

        contentQuerySet = Content.objects.all()

        for article in contentQuerySet:
            documents.append({'article_id': article.id, 'content': article.content, 'title': article.title,
                              'author': article.author, 'publisher': article.publisher, 'date': str(article.date)})

        index.delete_all_documents()
        index.add_documents(documents)

        return Response({'completed': True})


class CheckToken(views.APIView):
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class VersionInformation(views.APIView):
    def get(self, request):
        return Response({'version': settings.VERSION})

class ExportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        contentQuerySet = Content.objects.all()

        contentArray = [{
            'content_type': article.content_type,
            'url': article.url if article.url else None,
            'author': article.author if article.author else None,
            'publisher': article.publisher if article.publisher else None,
            'date': str(article.date) if article.date else None,
            'title': article.title,
            'content': article.content,
            'richtext': article.richtext,
        } for article in contentQuerySet]

        response = HttpResponse(json.dumps(contentArray), content_type='text/json')
        response['Content-Disposition'] = "attachment; filename=herodotus_export.json"

        return response

class ImportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        uploadedContent = request.FILES.get("content").read().decode('utf-8').replace("\n", '')
        parsed = json.loads(uploadedContent)

        for article in parsed:
            print(article['title'])
            contentObj = Content(title=article['title'], url=article['url'], content_type=article['content_type'], author=article['author'], publisher=article['publisher'], date=article['date'], content=article['content'], richtext=article['richtext'])
            contentObj.save()

        return HttpResponse("success")

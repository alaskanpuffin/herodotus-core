from .models import Content, User
from .serializers import ContentSerializer, ScrapedArticleSerializer, UserSerializer
from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from newspaper import Article
from rest_framework import permissions
from .pagination import ContentPagination
from django.db.models import Case, When
import meilisearch


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.order_by('-id')
    serializer_class = ContentSerializer
    pagination_class = ContentPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SearchContent(generics.ListCreateAPIView):
    pagination_class = ContentPagination
    serializer_class = ContentSerializer
    queryset = Content.objects.all()

    def list(self, request):
        search_ids = []

        search = request.GET.get('q')
        
        client = meilisearch.Client('http://192.168.0.25:7700')
        index = client.get_index('article')

        results = index.search(search)

        for result in results['hits']:
            search_ids.append(result['article_id'])

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(search_ids)])
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


class CheckToken(views.APIView):
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

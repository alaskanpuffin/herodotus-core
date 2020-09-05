from .models import Content
from .serializers import ContentSerializer, ScrapedArticleSerializer
from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from newspaper import Article
from rest_framework import permissions

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
            
        data= {"url": url, "title": article.title, "content": article.text, "author": article.authors, "date": article.publish_date}

        results = ScrapedArticleSerializer(data, many=False).data
        return Response(results)
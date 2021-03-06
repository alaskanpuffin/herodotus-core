"""herodotus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from .views import ImportView, ExportView, ContentViewSet, TagViewSet, ScrapeArticle, CheckToken, UserViewSet, SearchContent, IndexArticles, FeedViewSet, VersionInformation
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'content', ContentViewSet)
router.register(r'tag', TagViewSet)
router.register(r'user', UserViewSet)
router.register(r'feed', FeedViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrapearticle/', ScrapeArticle.as_view()),
    path('indexarticles/', IndexArticles.as_view()),
    path('version/', VersionInformation.as_view()),
    path('export/', ExportView.as_view()),
    path('import/', ImportView.as_view()),
    path('search/', SearchContent.as_view()),
    path('checktoken/', CheckToken.as_view()),
    path('', include(router.urls)),
    re_path(r'api/auth/', include('knox.urls')),
]
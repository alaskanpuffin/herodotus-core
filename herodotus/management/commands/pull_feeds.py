from django.core.management.base import BaseCommand, CommandError
from herodotus.models import Feed, FeedHistory, Content
import os
import feedparser
from newspaper import Article
from django.utils import timezone


class Command(BaseCommand):
    help = 'Checks all feeds for new content.'

    def scrapeArticle(self, url):
        article = Article(url)
        article.download()
        article.parse()

        if not article.authors == []:
            article.authors = article.authors[0]
        else:
            article.authors = ""

        return {"title": article.title[:500], "content": article.text,
                "author": article.authors}

    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        contentObj = Content.objects.all()
        feedHistoryObj = FeedHistory.objects.all()

        for feed in feeds:
            content = feedparser.parse(feed.url)
            for entry in content.entries:
                if not contentObj.filter(url=entry.link).exists() and not feedHistoryObj.filter(url=entry.link).exists():
                    article = self.scrapeArticle(entry.link)

                    date = entry.published_parsed
                    date = "%s-%s-%s" % (date[0], date[1], date[2])

                    articleObj = Content(
                        title=article['title'], content_type="article", publisher=feed.title, content=article['content'], url=entry.link, author=article['author'][:300], date=date)
                    feedHistoryEntryObj = FeedHistory(feed=feed, url=entry.link)
                    try:
                        articleObj.save()
                        feedHistoryEntryObj.save() # Prevent duplicate pulls if an article is deleted.
                    except:
                        print("Error saving article")

            # Update last updated time stamp on feed
            feed.last_updated = timezone.now()
            feed.save()

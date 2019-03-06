import requests
from django.conf import settings
from api.parsers import HackerNewsHtmlParser
from api.models import News

import logging

logger = logging.getLogger(__name__)


class HackerNewsSaver:
    def __init__(self):
        self._pairs = []

    def save(self):
        self._pairs = []
        self._get_pairs()
        self._check_pairs()
        self._save_pairs()

    @staticmethod
    def _get_content() -> str:
        response = requests.get(settings.HACKER_NEWS_URL)
        return response.text

    def _get_pairs(self):
        parser = HackerNewsHtmlParser()
        parser.feed(self._get_content())
        self._pairs = parser.pairs

    def _save_pairs(self):
        for news_pair in self._pairs:
            obj, created = News.objects.get_or_create(url=news_pair.url, title=news_pair.title)
            if created:
                logger.info('News "%s" was added', news_pair.title)
            else:
                logger.info('News "%s" already exists', news_pair.title)

    def _check_pairs(self):
        if len(self._pairs) == 0:
            msg = 'There is no one news.'
            logger.error(msg)
            raise RuntimeError(msg)

        if len(self._pairs) < settings.HACKER_NEWS_COUNT:
            logger.warn('Count of news less than %d. It is %d.', settings.HACKER_NEWS_COUNT, len(self._pairs))


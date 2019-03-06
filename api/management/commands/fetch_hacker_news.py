import logging

from django.core.management.base import BaseCommand

from api.services import HackerNewsSaver

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        HackerNewsSaver().save()

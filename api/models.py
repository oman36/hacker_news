from django.db import models


class News(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'url')

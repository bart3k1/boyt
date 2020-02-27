from django.contrib.auth.models import User
from django.db import models


class Row(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Movies(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    row = models.ForeignKey(Row, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

from __future__ import unicode_literals

from myrobogals.rgprofile.models import User
from django.db import models


# Create your models here.
class Tag(models.Model):
    tag = models.SlugField(max_length=20)

    def __str__(self):
        return str(self.tag)


class Article(models.Model):
    title = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    preview_text = models.CharField(max_length=350, default="")
    author = models.ForeignKey(User)
    url = models.SlugField(max_length=20)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    revision = models.IntegerField(default=-1)

    def save(self, *args, **kwargs):
        # Incrementing revision on every save
        self.revision += 1
        return super(Article, self).save(*args, **kwargs)
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
import re


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Post(TimeStampedModel):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(max_length=1000)

    def get_hash_tags(self):
        return re.findall(r'#[a-zA-Z0-9]+', self.content)

    def __str__(self):
        return "By {}, posted on {}".format(self.posted_by.get_full_name(), self.created)


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return "Tag {}".format(self.tag)

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Post(TimeStampedModel):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(max_length=500)

    def __str__(self):
        return "By {}, posted on {}".format(self.posted_by.get_full_name(), self.created)

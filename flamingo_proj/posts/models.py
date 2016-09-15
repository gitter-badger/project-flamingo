from __future__ import unicode_literals
import re


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
    content = models.TextField(max_length=1000, editable=True)

    def get_hash_tags(self):
        return re.findall(r'#[a-zA-Z0-9]+', self.content)

    @staticmethod
    def add_liked_by_user(set_of_posts, user):
        for post in set_of_posts:
            try:
                Like.objects.get(liked_by=user, post=post)
                post.liked_by_user = True
            except Like.DoesNotExist:
                post.liked_by_user = False
        return set_of_posts

    def __str__(self):
        return "Post by {}, posted on {}".format(self.posted_by.get_full_name(), self.created)


@python_2_unicode_compatible
class Share(TimeStampedModel):
    original_post = models.ForeignKey(Post)
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "Shared by {}".format(self.shared_by.get_full_name())


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return "Tag {}".format(self.tag)


@python_2_unicode_compatible
class Like(models.Model):
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='likes')

    def __str__(self):
        return "{} likes {}".format(self.liked_by, self.post)

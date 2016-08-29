from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from . import models


@receiver(post_save, sender=settings.AUTH_POST_MODEL)
def create_tags(sender, instance, created, **kwargs):
    old_refs = instance.tag_set.all()
    hash_tags = instance.get_hash_tags()
    for t in hash_tags:
        # Adding the new tags
        obj, created = models.Tag.objects.get_or_create(tag=t)
        obj.posts.add(instance)
        obj.save()

    old_refs = old_refs.exclude(tag__in=hash_tags)
    for old in old_refs:
        old.posts.remove(instance)
        old.save()

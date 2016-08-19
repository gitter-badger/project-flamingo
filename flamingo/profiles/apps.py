from __future__ import unicode_literals

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'
    verbose_name = 'User profiles'

    def ready(self):
        from . import signals

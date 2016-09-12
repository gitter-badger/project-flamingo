from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^feed/$', views.feed, name='feed'),
    url(r'^create/$', views.create_post, name='create_post')
]
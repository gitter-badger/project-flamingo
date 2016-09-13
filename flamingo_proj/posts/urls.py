from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.create_post, name='create_post'),
    url(r'^tag/(?P<tag>[a-zA-Z0-9]+)/$', views.posts_by_tag, name='tag'),
    url(r'^(?P<id>[0-9]+)/edit/$', views.post_edit, name='edit'),
    url(r'^(?P<id>[0-9]+)/delete/$', views.post_delete, name='delete'),
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.create_post, name='create_post'),
    url(r'^tag/(?P<tag>[a-zA-Z0-9]+)/$', views.posts_by_tag, name='tag'),
    url(r'^(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='detail'),
    url(r'^(?P<id>[0-9]+)/edit/$', views.post_edit, name='edit'),
    url(r'^(?P<id>[0-9]+)/delete/$', views.post_delete, name='delete'),
    url(r'^(?P<id>[0-9]+)/like/$', views.like, name='like'),
    url(r'^(?P<id>[0-9]+)/share/$', views.post_share, name='share'),
]

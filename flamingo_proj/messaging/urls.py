from django.conf.urls import url
from django.views.generic import RedirectView


from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox'), name='messages_redirect'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^outbox/$', views.outbox, name='outbox'),
    url(r'^compose/$', views.compose, name='compose'),
    url(r'^view/(?P<message_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^trash/$', views.trash, name='trash'),
]

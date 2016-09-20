from django.conf.urls import url
from django.views.generic import RedirectView


from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox'), name='messages-redirect'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^sent/$', views.sent, name='sent'),
    url(r'^compose/$', views.compose, name='compose'),
    url(r'^(?P<message_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<message_id>[0-9]+)/delete/$', views.delete_message, name='delete'),
    url(r'^trash/$', views.trash, name='trash'),
]

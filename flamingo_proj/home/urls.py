from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.sign_up, name='signup'),
    url(r'^search/$', views.search, name='search'),
]

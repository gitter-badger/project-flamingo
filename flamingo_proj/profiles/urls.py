from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views


urlpatterns = [
    url(r'^profile/$', views.CurrentProfile.as_view(), name='current-profile'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
]

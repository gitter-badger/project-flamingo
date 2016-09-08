from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views


urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'extra_context': {'next': '/accounts/profile/nomer/'}}),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
]

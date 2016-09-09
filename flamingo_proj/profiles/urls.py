from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^profile/$', views.GoToProfile.as_view(), name='go-to-profile'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.sign_up, name='sign_up'),
]

from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^providers/$', views.providers),
    url(r'^clients/$', views.clients),
    url(r'^client/(?P<pk>[0-9]+)/$', views.client),
    # url(r'^$', views.index, name='index'),
]
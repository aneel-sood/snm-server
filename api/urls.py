from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^providers/$', views.providers),
    url(r'^clients/$', views.clients),
    url(r'^client/(?P<pk>[0-9]+)/$', views.client),
    url(r'^client/(?P<client_id>[0-9]+)/needs/$', views.client_needs),
    url(r'^client/(?P<client_id>[0-9]+)/need/(?P<pk>[0-9]+)/$', views.client_need),
    # url(r'^$', views.index, name='index'),
]
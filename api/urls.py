from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^providers/$', views.providers),
    url(r'^clients/$', views.clients),
    url(r'^resources/$', views.resources),
    url(r'^dashboard/clients/$', views.dashboard_clients),
    url(r'^client/$', views.client),
    url(r'^client/(?P<pk>[0-9]+)/$', views.client),
    url(r'^client/(?P<client_id>[0-9]+)/needs/$', views.client_needs),
    url(r'^client/(?P<client_id>[0-9]+)/need/(?P<pk>[0-9]+)/$', views.client_need),
    url(r'^need/(?P<need_id>[0-9]+)/resource/(?P<pk>[0-9]+)/$', views.need_resource),
    # url(r'^$', views.index, name='index'),
]
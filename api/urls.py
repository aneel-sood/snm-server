from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
  url(r'^providers/$', views.ProviderList.as_view()),
  url(r'^provider/(?P<pk>[0-9]+)/$', views.ProviderDetail.as_view()),
  url(r'^resources/$', views.resources),
  url(r'^resource/$', views.resource),
  url(r'^resource/(?P<pk>[0-9]+)/$', views.resource),
  url(r'^providers/resources/search/$', views.provider_resource_search),
  url(r'^client/(?P<pk>[0-9]+)/$', views.ClientDetail.as_view()),
  url(r'^dashboard/clients/$', views.dashboard_clients),
  url(r'^client/(?P<client_id>[0-9]+)/needs/$', views.client_needs),
  url(r'^client/(?P<client_id>[0-9]+)/need/(?P<pk>[0-9]+)/$', views.client_need),
  url(r'^need/(?P<need_id>[0-9]+)/resource/(?P<pk>[0-9]+)/$', views.need_resource),
  # url(r'^$', views.index, name='index'),
]

urlpatterns = urlpatterns + format_suffix_patterns([
  url(r'^clients/$', views.ClientList.as_view()), 
  url(r'^needs/$', views.NeedList.as_view()), 
], allowed=['csv',])
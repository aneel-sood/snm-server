from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^resources/$', views.resources),
    url(r'^providers/$', views.providers),
    url(r'^providerss/$', views.all_providers),
    # url(r'^$', views.index, name='index'),
    # url(r'^interpreters/(?P<pk>[0-9]+)/$', views.interpreter_detail),
]
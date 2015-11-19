from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^just_testing/$', views.justTesting),
    url(r'^create_post/$', views.create_post),
    url(r'^create_comment/$', views.create_comment),
    url(r'^like_comment/$', views.like_comment),
    url(r'^threads/$', views.thread_list),
    url(r'^threads/(?P<myid>[0-9]+)/$', views.thread_detail),
    url(r'^threads/(?P<myid>[0-9]+)/comments/$', views.thread_comments),
]

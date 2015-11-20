from django.conf.urls import url, include
from rest_framework import routers
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # a quick test
    url(r'^just_testing/$', views.justTesting),
    # URL routes for creating threads and comments and liking comments 
    url(r'^create_post/$', views.create_post),
    url(r'^create_comment/$', views.create_comment),
    url(r'^like_comment/$', views.like_comment),
    # URL routes for REST api
    url(r'^threads/$', views.thread_list),
    url(r'^threads/(?P<myid>[0-9]+)/$', views.thread_detail),
    url(r'^threads/(?P<myid>[0-9]+)/comments/$', views.thread_comments),
]

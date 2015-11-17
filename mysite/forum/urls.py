from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^just_testing/$', views.justTesting),
    url(r'^create_post/$', views.create_post),
]

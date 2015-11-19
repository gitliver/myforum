from django.conf.urls import url, include
from rest_framework import routers
from . import views

# via http://www.django-rest-framework.org/tutorial/quickstart/
# router = routers.DefaultRouter()
# router.register(r'threads', views.ThreadViewSet)
# router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^just_testing/$', views.justTesting),
    url(r'^create_post/$', views.create_post),
    url(r'^threads/$', views.thread_list),
    url(r'^threads/(?P<myid>[0-9]+)/$', views.thread_detail),
    url(r'^threads/(?P<myid>[0-9]+)/comments/$', views.thread_comments),
    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

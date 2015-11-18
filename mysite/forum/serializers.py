from .models import Thread, Comment
from rest_framework import serializers

# modified from http://www.django-rest-framework.org/tutorial/quickstart/

class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thread
        fields = ('id', 'pub_date', 'title', 'username', 'description')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment 
        fields = ('id', 'pub_date', 'username', 'text', 'score')

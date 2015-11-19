from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from .models import Thread, Comment
from .forms import ThreadModelForm, CommentModelForm
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import ThreadSerializer, CommentSerializer
import json, datetime, pytz

# This code is written for an assignment, whose directions state:

# The "Forum" is a single-page application with the following functionality:
# The app has a Welcome page with a list of Threads
# The Welcome page also has a form where visitors can anonymously create new Threads (no need for a User model or for signup / authentication / etc)
# Clicking a Thread should bring up the "Thread Detail View"
# The Thread Detail View should show the Thread's child Comments and a form to (anonymously) submit a new Comment

def justTesting(request):
    """A test function, to ensure urls.py is routing properly"""
    return HttpResponse("Hello, world")

def index(request):
    """Main function that gets called when the user lands on the webpage"""

    # get forum thread objects, ordered by publication date
    # forumthreads = Thread.objects.order_by('pub_date')
    # get Thread form
    # form = ThreadModelForm()

    # render the page, passing a dict that holds the form as well as all threads
    # return render(request, 'forum/index.html', {'myform': form, 'mythreads': forumthreads})
    return render(request, 'forum/index.html')

def create_post(request):
    """Function to create thread (or post), called by Angular"""

    # see: http://django-angular.readthedocs.org/en/latest/angular-model-form.html
    if not request.is_ajax():
        return HttpResponseBadRequest('Expected an XMLHttpRequest')

    in_data = json.loads(request.body)

    # save in database
    # note that in_data.mytitle throws an error while in_data.get('mytitle') works smoothly
    post = Thread(pub_date = datetime.datetime.now(pytz.timezone('US/Eastern')), username = in_data.get('myusername'), title = in_data.get('mytitle'), description = in_data.get('mydescription'))
    post.save()

    return JsonResponse(in_data)

# Serializer classes for REST api
# modified from http://www.django-rest-framework.org/tutorial/quickstart/
# class ThreadViewSet(viewsets.ModelViewSet):
#     """API endpoint that allows users to be viewed or edited."""
# 
#     queryset = Thread.objects.all().order_by('-pub_date')
#     serializer_class = ThreadSerializer
# 
# class CommentViewSet(viewsets.ModelViewSet):
#     """API endpoint that allows groups to be viewed or edited."""
# 
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

# modified from: http://www.django-rest-framework.org/tutorial/1-serialization/
class drfJSONResponse(HttpResponse):
    """An HttpResponse that renders its content into JSON."""

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(drfJSONResponse, self).__init__(content, **kwargs)

# modified from: http://www.django-rest-framework.org/tutorial/1-serialization/
def thread_list(request):
    """List all forum threads."""

    if request.method == 'GET':
        mythreads = Thread.objects.all()
        serializer = ThreadSerializer(mythreads, many=True)
        return drfJSONResponse(serializer.data)

# modified from: http://www.django-rest-framework.org/tutorial/1-serialization/
def thread_detail(request, myid):
    """Thread detail view"""

    try:
        thread = Thread.objects.get(id=myid)
    except Thread.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return drfJSONResponse(serializer.data)

def thread_comments(request, myid):
    """Get the comments for a particular thread"""

    try:
	# get comments using the thread (foreign key) id
        mycomments = Comment.objects.filter(thread__id=myid)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # must use many=True or it throws error
        serializer = CommentSerializer(mycomments, many=True)
        return drfJSONResponse(serializer.data)

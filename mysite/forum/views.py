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
    return render(request, 'forum/index.html')

def create_post(request):
    """Function to create thread (or post), called by Angular"""

    # borrowed from:
    # http://django-angular.readthedocs.org/en/latest/angular-model-form.html

    if not request.is_ajax():
        return HttpResponseBadRequest('Expected an XMLHttpRequest')

    try:
        in_data = json.loads(request.body)
    except:
        return HttpResponseBadRequest('Error!')

    try:
        # save in database
        # note that in_data.mytitle throws an error while in_data.get('mytitle') works smoothly
        post = Thread(pub_date = datetime.datetime.now(pytz.timezone('US/Eastern')), username = in_data.get('myusername'), title = in_data.get('mytitle'), description = in_data.get('mydescription'))
        post.save()
    except:
        return HttpResponseBadRequest('Error saving to database!')

    return JsonResponse(in_data)

def create_comment(request):
    """Function to create comment, called by Angular"""

    # DRY violation vis a vis the prev function - could extract this out into common function - fix later
    if not request.is_ajax():
        return HttpResponseBadRequest('Expected an XMLHttpRequest')

    try:
        in_data = json.loads(request.body)
    except:
        return HttpResponseBadRequest('Error!')

    # get the Thread associated with the comments
    mythread = Thread.objects.get(id=in_data.get('mythreadid'))

    # save in database
    try:
        comment = Comment(pub_date = datetime.datetime.now(pytz.timezone('US/Eastern')), username = in_data.get('myusername'), text = in_data.get('mytext'), score = 0, thread = mythread )
        comment.save()
    except:
        return HttpResponseBadRequest('Error saving to database!')

    return JsonResponse(in_data)

def like_comment(request):
    """Function to 'like' a comment - i.e., increment its score"""

    if not request.is_ajax():
        return HttpResponseBadRequest('Expected an XMLHttpRequest')

    try:
        in_data = json.loads(request.body)
    except:
        return HttpResponseBadRequest('Error!')

    # increment comment score
    try:
        comment = Comment.objects.get(id=in_data.get('mycommentid'))
        comment.score += 1
        comment.save()
    except:
        return HttpResponseBadRequest('Error saving to database!')

    return JsonResponse(in_data)

class drfJSONResponse(HttpResponse):
    """An HttpResponse that renders its content into JSON."""
    # modified from: http://www.django-rest-framework.org/tutorial/1-serialization/

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(drfJSONResponse, self).__init__(content, **kwargs)

def thread_list(request):
    """Return all forum threads as JSON for the REST api"""
    # modified from: http://www.django-rest-framework.org/tutorial/1-serialization/

    if request.method == 'GET':
        mythreads = Thread.objects.all()
        serializer = ThreadSerializer(mythreads, many=True)
        return drfJSONResponse(serializer.data)

def thread_detail(request, myid):
    """Return forum thread of specific id as JSON for the REST api"""
    # modified from: http://www.django-rest-framework.org/tutorial/1-serialization/

    try:
        thread = Thread.objects.get(id=myid)
    except Thread.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return drfJSONResponse(serializer.data)

def thread_comments(request, myid):
    """Return all comments as JSON for a forum thread of specific id"""

    try:
	# get comments using the thread (foreign key) id
        mycomments = Comment.objects.filter(thread__id=myid)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # must use many=True or it throws error
        serializer = CommentSerializer(mycomments, many=True)
        return drfJSONResponse(serializer.data)
